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
0.2 ; Ajout de la notion de franchissable (attribut 'passable')

"""
__version__ = 0.2
import logging
import numpy as np
from parameters import DISTANCE, CATEG_COLORS, DISTANCE_POSITION, MAX_SPEED
from road_objects.graphical_item import GraphicalItem
from roadmaps.path import Path
from roadmaps.position import NONE_POSITION, Position


class RoadItem(GraphicalItem):
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
    _MAX_POSITION_FORWARD = int(np.ceil(MAX_SPEED/DISTANCE_POSITION))
    print(f"_MAX_POSITION_FORWARD = {_MAX_POSITION_FORWARD}")

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

    def __init__(self, axe, path=None, roads=None, name=None, **kwargs):
        """
        Initialiser l'objet RoadItem
        """
        super(RoadItem, self).__init__(axe)
        self._id = self._GetId()
        self.Add_item(self)

        self._name = name if name else f"{__class__.__name__}_{self.id}"
        """
        Le "f"blablabla{nomdelavariable}"blablabla" est un raccourci pour :
        ""blablabla{}blablabla".format(nomdelavariable)" 
        """
        logging.debug(f"Nouvel item de la classe {__class__.__name__} : {self.name}")
        self._current_time = kwargs.get('current_time', 0)
        self._init_time = kwargs.get('init_time', 0)
        self._delta_time = 0
        self._current_position_idx = kwargs.get('index', 0)
        self._passable = kwargs.get('passable', False)

        self.init_graphic()

        # Itinéraire à prendre par l'objet RoadItem
        if isinstance(path, Path):
            self.path = path
        elif isinstance(roads, list):
            self.path = Path(roads)
        else:
            self.path = Path()

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

    def __le__(self, other):
        """
        Test si self a une position avant un autre objget dans le parcours de self.
        :return:
            - True : si <other> est sur une position à venir de l'itinéraire de <self>
            - False : si
                -> <other> n'a pas de postion commune avec <self>
                -> <other> n'a pas démarré
                -> <self> n'a pas démarré
        """
        if not other.is_running or not self.is_running:
            return False
        else:
            return other.position in self.path[self._current_position_idx:]

    def init_graphic(self):
        """
        Initialise la représentation graphique
        """
        self.add_plot([], [], 'b', name="Point", label=self.name, marker='o')

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

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path:Path):
        """
        Affecte un itinéraire au véhicule
        """
        self._path = path

    @property
    def passable(self):
        """Retour le statut de franchissement"""
        return self._passable

    def set_passable(self, mode=True):
        """
        Change le statut de franchissement:
        - True : rend RoadItem franchissable (par défaut)
        - False : rend RoadItem infranchissable
        """
        logging.debug(f"{repr(self)} : Change 'Passable' from {self._passable} to {mode}")
        self._passable = mode

    def set_impassable(self):
        """Rend RoadItem infranchissable"""
        self.set_passable(False)

    @property
    def is_running(self):
        return self.is_started and not self.is_ended

    @property
    def index(self):
        return self._current_position_idx

    @index.setter
    def index(self, value):
        self._current_position_idx = int(value)

    @property
    def is_ended(self):
        return self.index >= len(self.path)

    @property
    def length(self):
        return len(self.path)

    @property
    def is_started(self):
        return self._current_position_idx>=0

    @property
    def position(self):
        if self._current_position_idx>=0 and self._current_position_idx<self.length:
            return self._path[self._current_position_idx]

    @property
    def next_position(self):
        """Retourne la position estimée de la prochaine frame"""
        return self.position

    def add_road(self, *road):
        """
        Ajoute une route à l'itinairaire
        """
        for road in roads:
            self._path.add_road(road)

    def remain_path(self, end_index=None):
        return self.path[max(0, min(self.index+1, self.length-1)):end_index] if not self.is_ended else []


    def start(self, init_time):
        """
        Définit le moment du départ
        => permet un décalage dans la lecture des positions
        """
        self._init_time = init_time
        self.current_time = 0
        self.index = -init_time

    def get_plot(self, new_time=None):
        """
        Retourne les éléménts graphique à afficher
        """
        if new_time is not None:
            self.forward(new_time)

        if self.position:
            self["Point"].set_data([self.position.x], [self.position.y])

        return self.get_components() if self.position else []

    def get_position(self, new_time):
        """
        Retourne la position (x,y) du Vehicule
        """
        self.forward(new_time)
        return NONE_POSITION if not self.is_started or self.is_ended else self.position

    def distance(self, position:Position)->float:
        """
        Calcul la distance entre <self> et l'objet <item>

        Pré-requis de construction : la distance entre chaque position est constante et vaut parameters.DISTANCE_POSITION
        distance ::=  (nb positions entre self et position) *


        <<<
        ancien mode de calcul =>
        distance ::= SUM( DISTANCE(postion_i, position_i+1) ), avec position_i in[self.position, item.position [
        La fonction de calcul de distance entre 2 positions est défini par le fonction DISTANCE
        >>>

        :return:
            - distance(self, item) si <item> a au moins une position commune avec <self>
            - None si pas de position commune
        """
        if position in self.remain_path(self.index+self._MAX_POSITION_FORWARD): #
            return (self.path.index(position) - self.index)* DISTANCE_POSITION
        else:
            return None

    def forward(self, new_time):
        """
        Methode par pdéfaut pour faire avancer un objet dans le temps
        """
        self.current_time = new_time