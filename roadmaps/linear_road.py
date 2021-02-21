"""
Project name : TIPE_Yoann
Module name : linear_road.py

Classes list in this module: 
- LinearRoad
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 21/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""
from roadmaps.map import Map
import numpy as np
from roadmaps.path import Path
from roadmaps.road import Road


class LinearRoad(Map):
    def __init__(self, axe):
        super(LinearRoad, self).__init__(axe)
        self.init_graphic()
        self.init_road()

    def init_graphic(self):
        self._ax.set_xlim(-20, 20)
        self._ax.set_ylim(-2, 2)

    def init_road(self):
        x_min, x_max = self._ax.get_xlim()
        self._roadmap = [
            Path(Road(
                x_interval=(x_min, x_max),
                y_interval=(0, 0),
                path_functions=(lambda x: x,lambda y: y),
                step=500
            ))
        ]

    def landscape(self):
        x_min, x_max = self._ax.get_xlim()
        artists = []
        artists.extend(self._ax.plot([x_min, x_max], [1, 1], 'b'))
        artists.extend(self._ax.plot([x_min, x_max], [-1, -1], 'b'))
        return artists
