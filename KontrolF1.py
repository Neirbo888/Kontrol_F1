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
            self.vumeters = [ VUMeterF1(self, [0 + index * 4, 1 + index * 4, 2 + index * 4, 3 + index * 4], index) for index in range(4) ]

    def update_display(self):
        for index in range(4):
            self.vumeters[index].update()
