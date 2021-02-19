"""
Ce module contient les routes permettant au véhicule de se déplacer
- Class road
- variable roadmap

"""
import numpy as np
from roadmaps.position import Position


class Road(object): # Même que "class Road():" ou "class Road:"
    """
    Définit la fonction de calcul de la trajectoire entre deux positions.
    """

    def __init__(self, x_interval, y_interval, path_functions, step=500):
        """
        x_interval : Intervalle de calcul (x_start, x_end)
        y_interval : Intervalle de calcul (y_start, y_end)
        path_functions : fonctions paramétriques (x_func, y_func)
            de calcul de la trajectoire entre les deux positions
        """
        self.x_interval = x_interval
        self.y_interval = y_interval
        self.path_functions = path_functions
        self.step = step
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
