"""
Module name : `path.py`
----------------------------
*Created on* 14/02/2021 *by* Eric Ollivier

*Versionning :*

* 0.1 : Initial version
* 0.2 : Ajout de la méthode 'append_position' permettant d'ajouter une position à un chemin
"""
__version__ = 0.2

from roadmaps.position import Position
from roadmaps.road import Road


class Path():
    def __init__(self, *roads):
        """
        :param roads: liste des routes (objet `roadmaps.Road`)
        
        *Note :* 
        
        Pour rappel, l'astérisque devant "roads" indique que la fonction peut prendre un nombre indéterminé de
        paramètres qui sont ensuite stockés dans une liste que l'on nomme "roads".
        """
        self._path=list()
        for road in roads:
            self.add_road(road)

    def add_road(self, road: Road):
        """
        Ajoute une route à l'itinéraire
        
        :param road: route (objet `roadmaps.road.Road`) à ajouter.
        """
        self._path.extend(road.path[:-1])
        # La méthodede liste "extend(iterable)" ajoute tous les éléments de l'itérable pris individuellement dans la
        # liste.

    def __len__(self):
        """
        Retourne le nombre de positions du chemin
        """
        return len(self._path)

    def __getitem__(self, index)->Position:
        """
        Retourne la position correspondant à l'index
        
        :param index: index de la position à retourner
        :type index: type `int` ou `slice`
        :return: un objet ou une liste d'objets `Position` correspondant à l'index
        :rtype: 
           * `Position` si un seul objet correspont à l'index, 
           * `list` (d'objets ) si plusieurs objets ocrrespond à `index`
        :except IndexError: si `ìndex` est en dehors des bornes de la liste `self._path`
        
        *Exemple :*
          *  si chemin = Path(...)
          *  `chemin[i]` retourne  l'objet `Position`  qui se trouve à la position `i+1` (index `i`) dans `chemin`
        """
        if isinstance(index, slice):
            return self._path[index] # TODO : Protéger en contrôlant l'index
        elif isinstance(index, int):
            if index >= 0 and index < len(self):
                return self._path[index]
            else:
                raise IndexError(f"{__class__}.__getitem__ : Index ({index}) is out of range.")

    def __contains__(self, item:Position):
        """
        Teste si une position fait partie de l'itinéraire
        
        :param item: objet `Position` à tester
        :return: Résultat du test d'appartenance :
        
        * `True` si `item` fait partie du chemin (`self._path`)
        * `False` sinon.
        
        *Usage :*  <objet de type Position> **in** <objet de type Path>
        
        *Exemple :* 
        
        `if objet_position in objet_path:`
            `<condition vraie>`
        `else:`
            `<condition fausse>`
        """
        return item in self._path

    def index(self, position:Position)->int:
        """
        Retourne l'index d'une position dans le chemin
        
        :param position: position à rechercher dans le chemin
        :return: index de l'objet position
        """
        return self._path.index(position)

    def append_position(self, position:Position):
        """
        Ajoute une position à la fin du chemin
        
        :param positon: position à ajouter
        """
        self._path.append(position)