"""
Ce module contient les routes permettant au véhicule de se déplacer
- Class road
- variable roadmap

"""
import numpy as np
from parameters import DISTANCE, DISTANCE_POSITION
from roadmaps.position import Position

NB_SAMPLES = 100

class Road(object): # Même que "class Road():" ou "class Road:"
    """
    Définit la fonction de calcul de la trajectoire entre deux positions.
    """

    def __init__(self, x_interval, y_interval, path_functions, step=None):
        """
        x_interval : Intervalle de calcul (x_start, x_end)
        y_interval : Intervalle de calcul (y_start, y_end)
        path_functions : fonctions paramétriques (x_func, y_func)
            de calcul de la trajectoire entre les deux positions
        """
        self.x_interval = x_interval
        self.y_interval = y_interval
        self.path_functions = path_functions
        self.step = step if step else self.init_step()
        self.setup_path()

    def setup_path(self):
        """
        Calcule les coordonnées de la route
        """
        self.path = [Position(x,y) \
            for x, y in zip(
                self.path_functions[0](np.linspace(*self.x_interval, self.step)),
                self.path_functions[1](np.linspace(*self.y_interval, self.step))
                )]

    def init_step(self):
        """
        Calcul le nombre de pas pour avoir une distance de DISTANCE_POSTION
        """
        # Distance à vol d'oiseau
        # linear_distance = DISTANCE(
        #     Position(self.path_functions[0](self.x_interval[0]),
        #              self.path_functions[1](self.y_interval[0])),
        #     Position(self.path_functions[0](self.x_interval[1]),
        #              self.path_functions[1](self.y_interval[1])))
        # )

        # Estimation de la distance réel
        samples_position = [Position(x,y) \
            for x, y in zip(
                self.path_functions[0](np.linspace(*self.x_interval, NB_SAMPLES)),
                self.path_functions[1](np.linspace(*self.y_interval, NB_SAMPLES))
                )]
        real_distance = sum([DISTANCE(samples_position[i], samples_position[i+1]) \
                             for i in range(len(samples_position)-2)
                             ])

        return np.round(real_distance/DISTANCE_POSITION)