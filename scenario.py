"""
Ce module contient
- class Scenario => permet de calculer par anticipation la position des véhicules

"""

MAX_FRAMES = 10000   # Nombre maximum d'étape du scénario

class Scenario:
    """
    Calcul la position des véhicules avant l'animation

    """
    def __init__(self, traffic:list):
        self._traffic = traffic     # Liste des véhicule
        self._frames = list()       # liste des coordonnées pour le traffic pour une étapge
        self.create_frames()

    def __len__(self):
        return len(self.frame)

    @property
    def frame(self):
        return self._frames

    def add_frame(self, value:list)->None:
        self._frames.append(value)

    def create_frames(self):
        """
        Création des frames
        """
        num_frame = 0
        while not all([vehicule.is_ended for vehicule in self._traffic]) and num_frame < MAX_FRAMES:
            self.add_frame([x.get_position(num_frame) for x in self._traffic])
            num_frame +=1

    def get_data(self, num_frame:int)->tuple:
        """
        Retour la série de coordonnées pour l'animation
        :return: ([x0, ...xn], [y0, ..., yn])
        """
        return (
            [x for x,y in self.frame[num_frame]],
            [y for x, y in self.frame[num_frame]]
        )