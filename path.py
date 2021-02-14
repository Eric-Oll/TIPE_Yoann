"""
Project name : TIPE_Yoann
Module name : path.py

Classes list in this module: 
- Path
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 14/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""
from position import Position
from road import Road


class Path():
    def __init__(self, *roads):
        self._path=list()
        for road in roads:
            self.add_road(road)

    def add_road(self, road:Road):
        """
        Ajout une route à l'itinéraire
        """
        self._path = self._path.extend(road.path)

    def __len__(self):
        return len(self._path)

    def __getitem__(self, index):
        """
        Retour la position correspondant à l'index
        """
        if index>=0 and index<len(self):
            return self._path[index]
        else:
            raise IndexError(f"{__class__}.__getitem__ : Index ({index}) is out of range.")

    def __contains__(self, item:Position):
        """
        Teste si une position fait partie de l'itinéraire

        usage : <objet de type Position> in <objet de type Path>
        """
        return item in self._path

