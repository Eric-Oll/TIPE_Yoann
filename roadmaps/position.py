"""
Project name : TIPE_Yoann
Module name : position.py

Classes list in this module: 
- Position
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 14/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""


class Position:
    """
    Classe définissant une position pour un objet RoadItem
    """
    _CHRONO = 0

    @classmethod
    def _Get_id(cls):
        """
        Donne un identifiant à une position
        """
        cls._CHRONO += 1
        return cls._CHRONO

    def __init__(self, x, y):
        self._id = self._Get_id()
        self._position = (x,y)

    def __repr__(self):
        return f"<Position ({self.x},{self.y})>"

    @property
    def id(self):
        return self._id

    @property
    def position(self):
        return self._position

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.id == other.id


# Définit l'objet pas de position
NONE_POSITION = Position(None, None)