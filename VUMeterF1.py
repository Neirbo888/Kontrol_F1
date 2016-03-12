#VUMeters.py
import LiveUtils
from _Framework.SliderElement import SliderElement
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller

CHANNEL_SCALE_MAX = 0.92
CHANNEL_SCALE_MIN = 0.52
MIDI_MAX_VALUE = 128

class VUMeterF1():
    'represents a single VU to store RMS values etc in'
    def __init__(self, parent, control_changes, track_index):
        self.buttons = [ SliderElement(MIDI_CC_TYPE, 2, index) for index in control_changes ]
        self.prev_values = [0] * len(control_changes)
        self.track_index = track_index
        self.parent = parent

    def update(self):
        if self.track_index >= len(LiveUtils.getTracks()):
            return

        track = LiveUtils.getTrack(self.track_index)

        vall = round(track.output_meter_left, 3) if track.has_audio_output else 0
        valr = round(track.output_meter_right, 3) if track.has_audio_output else 0

        level = (vall + valr) / 2
        if (level > CHANNEL_SCALE_MAX):
            level = CHANNEL_SCALE_MAX
        elif (level < CHANNEL_SCALE_MIN):
            level = CHANNEL_SCALE_MIN
        level = level - CHANNEL_SCALE_MIN
        level = (level * len(self.buttons) * MIDI_MAX_VALUE - 1) / (CHANNEL_SCALE_MAX - CHANNEL_SCALE_MIN)

        for slider_index in range(len(self.buttons)):
            slider_value = 0
            max_value = (slider_index + 1) * MIDI_MAX_VALUE - 1
            min_value = slider_index * MIDI_MAX_VALUE
            if (level >= max_value):
                slider_value = MIDI_MAX_VALUE - 1
            elif (level <= min_value):
                slider_value = 0
            else:
                slider_value = level - min_value
            if slider_value != self.prev_values[slider_index]:
                self.buttons[slider_index].send_value(slider_value, True)
                self.prev_values[slider_index] = slider_value
