#KontrolF1.py
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from VUMeterF1 import VUMeterF1


class KontrolF1(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self.__c_instance = c_instance
            self.log_message("Init")
            self.vumeter = VUMeterF1(self, [0, 1, 2, 3], 0)

    def update_display(self):
        self.vumeter.update()
