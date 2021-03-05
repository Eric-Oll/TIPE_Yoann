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

from road_objects.road_item import RoadItem
from roadmaps.path import Path
from roadmaps.position import Position


class TrafficLight(RoadItem):
    def __init__(self, position:Position, name=None):
        path = Path()
        path.append_position(position)
        super(TrafficLight, self).__init__(path=path, passable=False, index=0)
        logging.debug(f"TrafficLight : Création de {repr(self)} init. with postion {position}")

    def __repr__(self):
        return f"<TrafficLight: position={self.position}, passable={self.passable}, running={self.is_running}>"



