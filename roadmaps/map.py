"""
Project name : TIPE_Yoann
Module name : map.py

Classes list in this module: 
- Map : Classe de base pour les cartes
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 20/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""


class Map():
    def __init__(self, axe):
        self._ax = axe
        self._roadmap = None

    def landscape(self):
        """
        Fond de carte
        """
        raise NotImplemented

    @property
    def roadmap(self):
        """
        Liste des itinéraires
        """
        return self._roadmap

    @property
    def ax(self):
        return self._ax

    @property
    def xmin(self):
        return self.ax.get_xlim()[0]

    @property
    def xmax(self):
        return self.ax.get_xlim()[1]

    @property
    def ymin(self):
        return self.ax.get_ylim()[0]

    @property
    def ymax(self):
        return self.ax.get_ylim()[1]