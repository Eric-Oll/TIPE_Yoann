"""
Module name : `linear_road.py`
------------------------------
*Created on* 21/02/2021 *by* Eric Ollivier

*Classes list in this module:* 

* `LinearRoad`

*Versionning :*

* 0.1 : Initial version
* 0.2 : Simplification de la fonction 'landscape'
"""
__version__ = 0.2

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
        """
        Définit les paramètre graphique.
        - Taille du contexte grapghique
        - Borne des valeurs graphiques
        """
        self._ax.get_figure().set_size_inches(20,6)
        self._ax.set_xlim(0, 40)
        self._ax.set_ylim(-2, 2)
        self._artists = None

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
                # step=500
            ))
        ]

    def landscape(self):
        """
        Crée le fond de carte
        
        :return: liste des éléments composants le fond de carte.
        :rtype: objet `list` d'objets `matplotlib.Artist`
        """
        x_min, x_max = self._ax.get_xlim()
        artists = []
        artists.extend(self._ax.plot([x_min, x_max], [1, 1], 'b'))
        artists.extend(self._ax.plot([x_min, x_max], [-1, -1], 'b'))
        return artists
