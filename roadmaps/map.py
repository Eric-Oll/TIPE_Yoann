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