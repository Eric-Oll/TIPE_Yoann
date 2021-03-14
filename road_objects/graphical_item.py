"""
Module `graphical_item.py`
--------------------------
*Created on* 21/02/2021 *by* Eric Ollivier 

*Versioning :*   
- 0.1 : Initial version
"""
__version__ = '0.1'

from matplotlib.axes import Axes
from matplotlib.lines import Line2D


class GraphicalItem():
    """
    Représentation graphique des objets de la route
    """
    def __init__(self, axe:Axes):
        """
        :param axe: objet de type matplotlib.Axes (contexe graphique)
        """
        self._ax = axe
        self._components = dict()

    @property
    def ax(self):
        """Contexte graphique (objet de type `matplotlib.Axes`)"""
        return self._ax

    def __getitem__(self, name):
        """Retourne le composant graphique correspondant au nom `name`."""
        if name in self._components.keys():
            return self._components[name]
        else:
            raise KeyError(f"GraphicalItem.__getitem__ : key '{name}' inconnu.")

    def add_component(self, name:str, component):
        """
        Ajout un élement graphique de base pour la représentation de l'Item

        :param name: Nom du composant
        :param component: Composant à ajouter de type matplotlib.Artist
        """
        self._components[name] = component
        # if isinstance(component, Line2D):
        #     self.ax.add_line(component)

    def add_plot(self, *args, name:str, **kwargs):
        """
        Crée un objet grapghique avec la méthode `Axes.plot` et l'ajoute  à la liste des composants graphiques
        
        :param name: Nom à donner au nouveau composant
        :param args: Liste des paramètre pour la méthode `Axes.plot`
        :param kwargs: Liste des paramètres nommés pour la méthode `Axes.plot`
        """
        line, = self.ax.plot(*args, **kwargs)
        self.add_component(name, line)

    def get_components(self)->list:
        """
        Fournit la liste de composants graphique
        
        :returns: objet `list` d'objets de type matplotlib.Artist
        """
        return self._components.values()