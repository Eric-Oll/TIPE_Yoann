"""
Module name : `linear_road_with_traffic_light.py`
-------------------------------------------------
*Created on* 28/02/2021 *by* Eric Ollivier

*Classes list in this module:*
 
* linear_road_with_traffic_light

*Versionning :*

* 0.1 : Initial version
"""
__version__ = 0.1

from road_objects.traffic_light import TrafficLight
from roadmaps.map import Map
import numpy as np
from roadmaps.path import Path
from roadmaps.position import Position
from roadmaps.road import Road

class LinearRoadWithTrafficLight(Map):
    def __init__(self, axe):
        super(LinearRoadWithTrafficLight, self).__init__(axe)
        self.init_graphic()
        self.init_road()

    def init_graphic(self):
        """
        Définit les paramètre graphique.
        - Taille du contexte grapghique
        - Borne des valeurs graphiques
        """
        self._ax.get_figure().set_size_inches(20,6)
        self._ax.set_xlim(0, 80)
        self._ax.set_ylim(-2, 2)

    def init_road(self):
        """
        Crée l'objets de la route et définit l'itinéraire.
        """
        x_min, x_max = self._ax.get_xlim()
        self._roadmap = [
            Path(Road(
                x_interval=(x_min, x_max),
                y_interval=(0, 0),
                path_functions=(lambda x: x,lambda y: y),
            ))
        ]

        # Ajout d'un feu à mi-chemin
        real_position = self.roadmap[0][len(self.roadmap[0])//2]
        self.road_items.append(
            TrafficLight(
                axe=self.ax,
                position=real_position,
                graphic_position=Position(real_position.x, real_position.y-1.1)
            ),
        )

    def landscape(self):
        """
        Crée le fond de carte

        :return: liste des éléments composants le fond de carte.
        :rtype: objet `list` d'objets `matplotlib.Artist`
        """
        return [
            *self._ax.plot([self.xmin, self.xmax], [1, 1], 'b'),
            *self._ax.plot([self.xmin, self.xmax], [-1, -1], 'b')
        ]
