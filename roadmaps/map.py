"""
Module name : `map.py`
----------------------------
*Created on* 20/02/2021 *by* Eric Ollivier

*Versionning :*

* 0.1 : Initial version
"""


class Map():
    """
    Interface pour la création des cartes.

    *Cette classe ne peut pas être instanciée directement. Il est nécessaire de la dériver.*
    """
    def __init__(self, axe):
        self._ax = axe
        self._roadmap = None
        self._roaditems = list()

    def landscape(self):
        """
        Signature de la méthode de création du fond de carte
        
        **Méthode à implémenter dans la classe fille.**
        """
        raise NotImplemented

    @property
    def road_items(self)->list:
        """
        Liste des objets de la route.
        """
        return self._roaditems

    @property
    def roadmap(self)->list:
        """
        Liste des itinéraires
        """
        return self._roadmap

    @property
    def ax(self):
        """
        Contexte graphique 
        :return: objet matplotlib.Axes
        """
        return self._ax

    @property
    def xmin(self)->float:
        "Borne inférieure pour l'axe des abscisses"
        return self.ax.get_xlim()[0]

    @property
    def xmax(self)->float:
        "Borne supérieure pour l'axe des abscisses"
        return self.ax.get_xlim()[1]

    @property
    def ymin(self)->float:
        "Borne inférieure pour l'axe des ordonnées"
        return self.ax.get_ylim()[0]

    @property
    def ymax(self)->float:
        "Borne supérieure pour l'axe des ordonnées"
        return self.ax.get_ylim()[1]