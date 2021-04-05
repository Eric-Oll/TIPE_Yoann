"""
Module name : `position.py`
----------------------------
*Created on* 14/02/2021 *by* Eric Ollivier

### Liste des classes dans le module: 

* Position

### Constantes du module :

* `NONE_POSITION` : Objet de type `Position` correspondant à l'absence de position

*Versionning :*

* 0.1 : Initial version
"""
__version__ = "0.1"

class Position:
    """
    Classe définissant une position pour un objet RoadItem
    """
    _CHRONO = 0

    @classmethod
    def _Get_id(cls):
        """
        Donne un identifiant à une position
        """
        cls._CHRONO += 1
        return cls._CHRONO

    def __init__(self, x, y):
        """
        :param x: Abscisse de la position
        :param y: Ordonnée de la position
        """
        self._id = self._Get_id()
        self._position = (x,y)

    def __repr__(self):
        "Représentation de l'objet"
        return f"<Position #{self.id} ({self.x},{self.y})>"

    @property
    def id(self):
        "Identifiant de la position"
        return self._id

    @property
    def position(self)->tuple:
        """
        Coordonnées de la position sous la forme d'un tuple (<abscisse>, <ordonnée>)
        
        :rtype: (float, float)
        """
        return self._position

    @property
    def x(self)->float:
        """
        Abscisse de la postion
        
        :rtype: float
        """
        return self._position[0]

    @property
    def y(self)->float:
        """
        Ordonnée de la postion
        
        :rtype: float
        """
        return self._position[1]

    def __eq__(self, other):
        """
        Test si l'identifiant d'une position est égal à un autre
        
        :param other: objet de type `Position` à comparer avec `self`
        :return:
        * `True` : si les identifiants des deux objets (`self` et `other`) sont les mêmes
        * `False` sinon.
        """
        if isinstance(other, Position):
            return self.id == other.id


# Définit l'objet pas de position
NONE_POSITION = Position(None, None)