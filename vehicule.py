"""
Ce module contient la définition de la classe Vehicule
"""

class Vehicule(object):
    """
    Regroupe les routes  de son itinairaire
    et définit la position du véhicule dans le temps
    """

    def __init__(self, roads=None):
        self.init_time = 0
        self.path = [] # Liste des routes à prendre par le Vehicule
        if roads is not None:
            self.add_path(roads)

    @property
    def length(self):
        return len(self.path)

    @property
    def travel_time(self):
        return self.init_time + self.length

    def add_path(self, roads:list):
        """
        Ajoute une route à l'itinairaire
        """
        for road in roads:
            self.path.extend(road.path)

    def start(self, init_time):
        """
        Définit le moment du départ
        => permet un décalage dans la lecture des positions
        """
        self.init_time = init_time

    def get_position(self, current_time):
        """
        Retourne la position (x,y) du Vehicule
        """
        real_time = current_time-self.init_time
        return (None, None) if real_time<0 or real_time>= len(self.path) else self.path[real_time]
