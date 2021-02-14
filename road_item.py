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
    - Véhicule
    - obstable (à venir ?)
    - signalisation (ex : feux tricolores)
    - ...

    Contribue à calculer le changement de vitesse des véhicules
    """
    _COUNTER = 0
    _Item_list = list()

    @classmethod
    def _GetId(cls):
        """
        Le "cls" utilisé à la place du classique "self" indique qu'on travaille ici avec une méthode de classe :
        le "self" désigne un objet alors que "cls" désigne la classe elle-même.

        Conséquence : si on modifie la valeur pour un objet de la classe, cela le modifie pour tous les éléments de
        la classe.

        Exemple : on considère toto une méthode d'objet de la classe TTTT et tata une méthode de classe de TTTT et
        le code suivant :

        obj1 = TTTT()
        obj2 = TTTT()
        obj1.toto('x')
        obj2.toto('y')
        obj1.tata('X')
        obj2.tata('Y')
        print(obj1.toto, obj1.tata) >>> 'x','Y'
        Ici, la ligne 4 n'a pas modifié l'action de la ligne 3 car toto est une méthode qui s'applique et que les objets
        sont différents. En revanche, tata est une méthode de classe donc elle s'applique à tous les objets de la
        classe : c'est pourquoi la ligne 6 a modifié la ligne 5.
        """
        cls._COUNTER += 1
        return cls._COUNTER

    @classmethod
    def Add_item(cls, item):
        """
        Ajoute un objet à l'inventaire des items de la route
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
        self._name = name if name else f"{__class__.__name__}_{self.id}"
        """
        Le "f"blablabla{nomdelavariable}"blablabla" est un raccourci pour :
        ""blablabla{}blablabla".format(nomdelavariable)" 
        """
        logging.debug(f"Nouvel item de la classe {__class__.__name__} : {self.name}")
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
        Définit l'égalité pour la comparaison entre les objets
        """
        if isinstance(other, RoadItem):
            """
            La fonction isinstance" prend en arguments un objet et un type (ou plusieurs types) et renvoie un booléen
            indiquant si l'objet est de l'un de ces types.
            """
            return self.id == other.id
        else:
            return False

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter # C'est cette fonction qui sera appelée (et pas la précédente) quand on voudra modifier la
    # variable "current_time"
    def current_time(self, real_time):
        self._delta_time = real_time-self._current_time
        self._current_time = real_time

    @property
    def delta_time(self):
        return self._delta_time
