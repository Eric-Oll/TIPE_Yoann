"""
Project name : TIPE_Yoann
Module name : graphical_item.py

Classes list in this module: 
- GraphicalItem : Représentation graphique des objets de la route
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 21/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""
from matplotlib.lines import Line2D


class GraphicalItem():
    def __init__(self, axe):
        self._ax = axe
        self._components = dict()

    @property
    def ax(self):
        return self._ax

    def __getitem__(self, name):
        if name in self._components.keys():
            return self._components[name]
        else:
            raise KeyError(f"GraphicalItem.__getitem__ : key '{name}' inconnu.")

    def add_component(self, name, component):
        """
        Ajout un élement graphique de base pour la représentation de l'Item
        """
        self._components[name] = component
        if isinstance(component, Line2D):
            self.ax.add_line(component)

    def add_plot(self, *args, name:str, **kwargs):
        line, = self.ax.plot(*args, **kwargs)
        self.add_component(name, line)

    def get_components(self):
        """
        Retourne la liste de composants graphique
        """
        return self._components.values()