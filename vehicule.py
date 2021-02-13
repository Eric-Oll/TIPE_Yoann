"""
Ce module contient la définition de la classe Vehicule
"""

class Vehicule(object):
    """
    Regroupe les routes  de son itinairaire
    et définit la position du véhicule dans le temps
    """
    MAX_SPEED = 20

    def __init__(self, roads=None):
        self._init_time = 0
        self._current_speed = self.MAX_SPEED # On démarre avec la vitesse maximale
        self._current_time = 0
        self._current_position_idx = 0

        self._path = [] # Liste des routes à prendre par le Vehicule
        if roads is not None:
            self.add_path(roads)

    @property
    def length(self):
        return len(self._path)

    @property
    def travel_time(self):
        return self._init_time + self.length

    @property
    def is_ended(self):
        return self.index >= len(self._path)

    @property
    def index(self):
        return self._current_position_idx

    def add_path(self, roads:list):
        """
        Ajoute une route à l'itinairaire
        """
        for road in roads:
            self._path.extend(road.path)

    def start(self, init_time):
        """
        Définit le moment du départ
        => permet un décalage dans la lecture des positions
        """
        self._init_time = init_time
        self._current_time = - self._init_time

    def get_position(self, current_time):
        """
        Retourne la position (x,y) du Vehicule
        """
        real_time = current_time-self._init_time
        self._current_position_idx = real_time
        return (None, None) if real_time<0 or real_time>= len(self._path) else self._path[real_time]
