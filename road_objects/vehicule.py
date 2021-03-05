"""
Ce module contient la définition de la classe Vehicule

______________________________________________________________________________________________________________
Versions :
0.1 :
- Vehicule.index : cast la valeur en 'int'
"""
import logging

from road_objects.road_item import RoadItem, DISTANCE
from parameters import MAX_SPEED, MAX_SPEED_UP, MAX_SPEED_DOWN, MIN_DISTANCE, SPEED_START, MAX_SPEED_DOWN_FUNC, \
    MAX_SPEED_UP_FUNC, CATEG_COLORS


class Vehicule(RoadItem):
    """
    Regroupe les routes  de son itinairaire
    et définit la position du véhicule dans le temps
    """


    @classmethod
    def List_vehicules(cls):
        """
        Retourne la liste des véhicules
        """
        return [vehicule for vehicule in cls.Get_Items if isinstance(vehicule, Vehicule)]

    def __init__(self, axe, path=None, name=None):
        super(Vehicule, self).__init__(axe=axe, path=path, name=name)
        if name is None: self._name = f"Vehicle_{self.id}"
        self._init_time = 0
        self._current_speed = SPEED_START # On démarre avec la vitesse maximale

    def __repr__(self):
        return f"<Vehicule {self.name} : position={self.position}(index={self.index}), speed={self.speed}, length={self.length}>"

    @property
    def travel_time(self):
        return self._init_time + self.length

    @property
    def speed(self):
        return self._current_speed

    @speed.setter
    def speed(self, value):
        # logging.debug(f"Vehicule {self.name} : change speed from {self.speed} to {value}")
        self._current_speed = value

    @property
    def category(self):
        return int(self.speed)

    @property
    def next_position(self):
        return self.path[min(self.index + int(self.delta_time*self.speed), self.length-1)]

    def forward(self, new_time):
        # logging.debug(repr(self)+f".forward : ended={self.is_ended}")
        if not self.is_ended:
            # logging.debug(f"... new time = {new_time}")
            # logging.debug(f"... current time = {self.current_time}")
            self.current_time = new_time
            self.index += self.delta_time*self.speed if self.is_running else self.delta_time*MAX_SPEED
            # logging.debug(f"... delta time = {self.delta_time}")

    def update_speed(self, distance:float=None)->None:
        """
        Calcul et met à jour la vitesse en fonction de la distance de l'objet routier suivant
        :param distance: distance entre <self> et l'objet suivant
        """
        if not self.is_running : return
        if distance:
            ratio = DISTANCE(self.path[0], self.path[1])
            self.speed = min(MAX_SPEED,                                         # Vitesse maximal
                             max(MAX_SPEED_DOWN_FUNC(self.speed, distance),     # vitesse de décélération maximum
                                 min(MAX_SPEED_UP_FUNC(self.speed, distance),   # vitesse d'accélération maximal
                                     # SPEED_START,                               # Vitesse de démarrage
                                     max(0,                                     # Vitesse minimal
                                         (distance-MIN_DISTANCE)/ratio)         # Vitesse calculé
                                     )
                                 )
                         )
        else:
            self.speed = min(MAX_SPEED,                                  # Vitesse maximal
                             self.speed + self.speed * MAX_SPEED_UP      # vitesse d'accélération maximal
                         )

    def get_plot(self, new_time=None):
        """
        Retourne les éléménts graphique à afficher
        """
        if new_time is not None:
            self.forward(new_time)

        if self.position:
            self["Point"].set_data([self.position.x], [self.position.y])
            self["Point"].set_color(CATEG_COLORS[self.category])

        return self.get_components() if self.position else []