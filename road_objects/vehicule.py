"""
Module name : `road_item.py`
----------------------------
*Created on* 13/02/2021 *by* Eric Ollivier

*Versionning :*

* 0.1 : Initial version

> Vehicule.index : cast la valeur en 'int'
"""
import logging

from road_objects.road_item import RoadItem, DISTANCE
from parameters import MAX_SPEED, MAX_SPEED_UP, MAX_SPEED_DOWN, MIN_DISTANCE, SPEED_START, MAX_SPEED_DOWN_FUNC, \
    MAX_SPEED_UP_FUNC, CATEG_COLORS, DISTANCE_POSITION


class Vehicule(RoadItem):
    """
    Représente un objet roulant (itinéraire, postion et vitesse).
    Regroupe les routes de son itinairair et définit la position du véhicule dans le temps
    """

    @classmethod
    def List(cls):
        """
        Retourne la liste des véhicules
        """
        return (vehicule for vehicule in cls.Get_Items() if isinstance(vehicule, Vehicule))

    def __init__(self, axe, path=None, name=None):
        """
        :param axe: contexte graphique
        :type axe: matplotlib.Axes
        :param path: Itinéraire du véhicule (par défaut None)
        :type path: list<Position>
        :param name: Nom du véhicule. Par défaut "Vehicle_<identifiant auto>"
        :type name: str
        """
        super(Vehicule, self).__init__(axe=axe, path=path, name=name)
        
        if name is None: self._name = f"Vehicle_{self.id}"
        self._init_time = 0
        self._current_speed = SPEED_START # On démarre avec la vitesse maximale

    def __repr__(self):
        "Représentation textuel du véhicule"
        return f"<Vehicule {self.name} : position={self.position}(index={self.index}), speed={self.speed}, length={self.length}>"

    @property
    def travel_time(self):
        return self._init_time + self.length

    @property
    def speed(self):
        "Vitesse du véhicule"
        return self._current_speed

    @speed.setter
    def speed(self, value):
        if self._current_speed!= value :
            logging.debug(f"Vehicule {self.name} : change speed from {self.speed} to {value}")
        self._current_speed = value

    @property
    def category(self):
        """
        Catégorie du véhicule. Permet de définir la couleur du véhicule au niveau de l'affichage.
        
        La couleur change en fonction de la vitesse.
        """
        return int(self.speed)

    @property
    def next_position(self):
        """
        Retourne la position suviante estimée du véhicule (t+1 sans changement de vitesse)
        
        :rtype: Position 
        """
        return self.path[
            max(0,
                min(
                    self.index + int(self.delta_time*self.speed),
                    self.length-1,
                    )
                )
            ]

    def forward(self, new_time:int):
        """
        Cette méthode calcule les nouvelles coordonnées du véhicule pour le temps `new_time`.
        
        :param new_time: Temps absolu dans le scénario.
        :type new_time: int
        """
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
        :type distance: float
        """
        if not self.is_running : return
        if distance:
            self.speed = min(MAX_SPEED,                                         # Vitesse maximal
                             max(MAX_SPEED_DOWN_FUNC(self.speed, distance),     # vitesse de décélération maximum
                                 min(MAX_SPEED_UP_FUNC(self.speed, distance),   # vitesse d'accélération maximal
                                     # SPEED_START,                             # Vitesse de démarrage
                                     max(0,                                     # Vitesse minimal
                                         (distance-MIN_DISTANCE)/DISTANCE_POSITION)         # Vitesse calculé
                                     )
                                 )
                         )
            logging.debug(f"{repr(self)} : new speed {self.speed} for distance={distance}.")
        else:
            self.speed = min(MAX_SPEED,                                       # Vitesse maximal
                             MAX_SPEED_UP_FUNC(self.speed, MIN_DISTANCE*100)  # vitesse d'accélération maximal
                         )
            logging.debug(f"{repr(self)} : new speed without distance")

    def get_plot(self, new_time:int=None)->list:
        """
        Retourne les éléménts graphique à afficher
        
        :param new_time: Temps absolu dans le scénario. 
        :type new_time: int ou None
        
        * Si valeur entière, on fait avancer le véhicule. 
        * Si `None`, le véhicule ne bouge pas. (valeur par défaut).
        
        :return: Liste des composant grapgique pour le raffraichissement de l'image
        :rtype: list<matplotlib.artist.Artist>
        """
        if new_time is not None:
            self.forward(new_time)

        if self.position:
            self["Point"].set_data([self.position.x], [self.position.y])
            self["Point"].set_color(CATEG_COLORS[self.category])

        return self.get_components() if self.position else []