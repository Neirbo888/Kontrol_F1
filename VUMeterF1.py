#VUMeters.py
import LiveUtils
from _Framework.SliderElement import SliderElement
from _Framework.InputControlElement import *
import ColorMap

CHANNEL_SCALE_MAX = 1
CHANNEL_SCALE_MIN = 0.2

class VUMeterF1:
    'represents a single VU to store RMS values etc in'
    def __init__(self, parent, control_changes, track_index):
        Disconnectable.__init__(self)
        self.resolution = len(control_changes)
        self.sliderHue = [ SliderElement(MIDI_CC_TYPE, 0, index) for index in control_changes ]
        self.sliderSatu = [ SliderElement(MIDI_CC_TYPE, 1, index) for index in control_changes ]
        self.sliderLight = [ SliderElement(MIDI_CC_TYPE, 2, index) for index in control_changes ]
        self.previousHue = [-1] * self.resolution
        self.previousSatu = [-1] * self.resolution
        self.previousLight = [-1] * self.resolution
        self.track_index = track_index
        self.parent = parent


    def update(self):
        if self.track_index >= len(LiveUtils.getTracks()):
            return

        track = LiveUtils.getTrack(self.track_index)
        colorIndex = track.color_index

        colorHue = ColorMap.hue[colorIndex]
        colorSatu = ColorMap.saturation[colorIndex]
        colorLight = ColorMap.light[colorIndex]

        valLeft = round(track.output_meter_left, 3) if track.has_audio_output else 0
        valRight = round(track.output_meter_right, 3) if track.has_audio_output else 0

        level = (valLeft + valRight) / 2
        if (level > CHANNEL_SCALE_MAX):
            level = CHANNEL_SCALE_MAX
        elif (level < CHANNEL_SCALE_MIN):
            level = CHANNEL_SCALE_MIN
        level = level - CHANNEL_SCALE_MIN
        level = (level / (CHANNEL_SCALE_MAX - CHANNEL_SCALE_MIN)) * self.resolution

        for index in range(self.resolution):
            max_value = index + 1
            min_value = index
            if (level <= min_value):
                colorLight = 0
            elif (level < max_value):
                colorLight = (level - min_value) * colorLight

            if colorHue != self.previousHue[index]:
                self.sliderHue[index].send_value(colorHue, True)
                self.previousHue[index] = colorHue
            if colorSatu != self.previousSatu[index]:
                self.sliderSatu[index].send_value(colorSatu, True)
                self.previousSatu[index] = colorSatu
            if colorLight != self.previousLight[index]:
                self.sliderLight[index].send_value(colorLight, True)
                self.previousLight[index] = colorLight
