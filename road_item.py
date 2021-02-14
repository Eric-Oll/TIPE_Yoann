"""
Project name : TIPE_Yoann
Module name : road_item.py

Classes list in this module: 
- RoadItem
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 14/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""
import logging


class RoadItem:
    """
    Classe de base pour les objets de la route :
    - Vehicule
    - obstable (à venir ?)
    - signalisation (ex. feux tricolores)
    - ....

    Contribue de calculer la changement de vitesse des véhicules
    """
    _COUNTER = 0
    _Item_list = list()

    @classmethod
    def _GetId(cls):
        cls._COUNTER += 1
        return cls._COUNTER

    @classmethod
    def Add_item(cls, item):
        """
        Ajout un objet à l'inventaire des items de la route
        """
        cls._Item_list.append(item)

    @classmethod
    def Get_Items(cls):
        """
        Retourne la liste des items
        """
        return cls._Item_list

    def __init__(self, name=None):
        self._id = self._GetId()
        self._name = name if name  else f"{__class__.__name__}_{self.id}"
        logging.debug(f"Nouvel item de la class {__class__.__name__} : {self.name}")
        self._current_time = 0
        self._delta_time = 0
        self.Add_item(self)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        """
        Défini l'égalité pour la comparaison entre les objets
        """
        if isinstance(other, RoadItem):
            return self.id == other.id
        else:
            return False

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, real_time):
        self._delta_time = real_time-self._current_time
        self._current_time = real_time

    @property
    def delta_time(self):
        return self._delta_time
