"""
Project name : TIPE_Yoann
Module name : traffic_light.py

Classes list in this module: 
- TrafficLight : Simule un feu tricolore
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 28/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""
import logging

from parameters import PASSABLE_TIME, CYCLE_TIME
from road_objects.road_item import RoadItem
from roadmaps.path import Path
from roadmaps.position import Position


class TrafficLight(RoadItem):
    def __init__(self, axe, position:Position, graphic_position:Position, name=None):
        path = Path()
        path.append_position(position)
        self._graphic_position = graphic_position
        super(TrafficLight, self).__init__(axe=axe, path=path, passable=False, index=0)
        logging.debug(f"TrafficLight : Création de {repr(self)} init. with postion {position}")

    def __repr__(self):
        return f"<TrafficLight: position={self.position}, passable={self.passable}, running={self.is_running}>"

    def init_graphic(self):
        """
        Initialise la représentation graphique
        """
        self.add_plot([self._graphic_position.x], [self._graphic_position.y], 'b',
                      name="Signal",
                      label=self.name,
                      marker='o',
                      )

    @property
    def is_running(self):
        return True

    def forward(self, new_time):
        """
        Methode par pdéfaut pour faire avancer un objet dans le temps
        """
        self.current_time = new_time

        self.set_passable((self.current_time+self._init_time) % CYCLE_TIME <=PASSABLE_TIME)

        if self.passable:
            self["Signal"].set_color('g')
        else:
            self["Signal"].set_color('r')

    def get_plot(self, new_time):
        """
        Retourne les éléménts graphique à afficher
        """
        if new_time is not None:
            self.forward(new_time)

        return self.get_components()
