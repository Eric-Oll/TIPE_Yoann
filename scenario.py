"""
Ce module contient
- class Scenario => permet de calculer par anticipation la position des véhicules

"""
import logging

from road_objects.road_item import RoadItem

MAX_FRAMES = 10000   # Nombre maximum d'étape du scénario

class Scenario:
    """
    Calcule la position des véhicules avant l'animation

    """
    def __init__(self, traffic: list, axe):
        self._ax = axe              # Axes de matplotlib pour l'affichage
        self._traffic = traffic     # Liste des véhicules
        self._frames = list()       # liste des coordonnées pour le traffic pour une étape
        # self.create_frames()

    def __len__(self):
        return len(self.frames)

    def __call__(self, frame):
        """
        Fonction appelé pour l'affichage des Frames
        """
        print(f"Frame #{frame} : Nb vehicule running = {len([vehicule for vehicule in self._traffic if vehicule.is_running])}")
        # logging.debug(f"Frame #{frame}/{len(self)} : Items of Frame {self.frames[frame]}")

        logging.debug(f"""Frame #{frame} : {[f"{vehicule.is_started}({vehicule.index}) / Categ.={vehicule.category}"
                                                 for vehicule in self._traffic]}""")

        # Mise à jour de la vitesse des véhicule
        for vehicule in self._traffic:
            logging.debug(f"Frame #{frame} : Update Speed for {vehicule.name} ...")
            if vehicule.is_running:
                list_distance = []
                for item in [item for item in vehicule.Get_Items() if item.is_running and vehicule != item]:
                    d = vehicule.distance(item.next_position)
                    if d is not None:
                        list_distance.append(d)
                logging.debug(
                    f"Frame #{frame} : Update Speed for {vehicule.name} : distance with other {list_distance}")
                if len(list_distance) > 0:
                    vehicule.update_speed(min(list_distance))
                else:
                    vehicule.update_speed()

        artists = []
        for item in RoadItem.Get_Items():
            item.forward(frame)
            if item.is_running:
                artists.extend(item.get_plot(ax=self._ax))

        logging.debug(f"Frame #{frame} : Items of Axes {[line.get_data() for line in self._ax.lines]}")
        logging.debug(f"Frame #{frame} : Items of Artists {[line.get_data() for line in artists]}")

        return [item for item in artists if item is not None]

    @property
    def frames(self):
        return self._frames

    def get_sequence(self):
        num_frame = 0
        while not all([vehicule.is_ended for vehicule in self._traffic]) and num_frame < MAX_FRAMES:
            yield num_frame
            num_frame += 1
        print("End of movie.")


    def add_frame(self, value: list) -> None:
        """
        Le ":list" indique le type (ici, le type list) d'une variable en paramètre d'une fonction (ici, la variable
        "value") et le "->None" indique la signature de la fonction (ce qu'elle renvoie) : ici, par exemple, elle ne
        renvoie rien (donc elle est de type None).
        """
        self._frames.append(value)

    def create_frames(self):
        """
        Création des frames
        """
        num_frame = 0
        while not all([vehicule.is_ended for vehicule in self._traffic]) and num_frame < MAX_FRAMES:
            """
            La fonction "all" est une fonction qui prend une liste de booléens en paramètre et renvoie True si tous les
            booléens de la liste sont True (cf. "pour tout" mathématique).
            Il existe une sorte de fonction contraire : il s'agit de la fonction "any" : elle prend également une liste
            de booléens en paramètre et renvoie True si au moins l'un des booléens est égal à True (cf. "il existe"
            mathématique).
            """
            logging.debug(f"""Frame #{num_frame} : {[f"{vehicule.is_started}({vehicule.index}) / Categ.={vehicule.category}" 
                                                     for vehicule in self._traffic]}""")

            # Mise à jour de la vitesse des véhicule
            for vehicule in self._traffic:
                logging.debug(f"Frame #{num_frame} : Update Speed for {vehicule.name} ...")
                if vehicule.is_running:
                    list_distance = []
                    for item in [item for item in vehicule.Get_Items() if item.is_running and vehicule != item]:
                        d = vehicule.distance(item.next_position)
                        if d is not None:
                            list_distance.append(d)
                    logging.debug(f"Frame #{num_frame} : Update Speed for {vehicule.name} : distance with other {list_distance}")
                    if len(list_distance) > 0:
                        vehicule.update_speed(min(list_distance))
                    else:
                        vehicule.update_speed()

            artists = []
            for item in RoadItem.Get_Items():
                item.forward(num_frame)
                if item.is_running:
                    artists.extend(item.get_plot(ax=self._ax))

            self.add_frame(artists)
            num_frame += 1

    def get_data(self, num_frame: int, category=None) -> tuple:
        """
        Retourne la série de coordonnées pour l'animation
        :param num_frame: N° de la frame
        :category: filtre sur la catégorie du véhicule.
            Par défaut None = tous les véhicules.
        :return: ([x0, ...xn], [y0, ..., yn])
        """
        return (
            [position.x for position, categ in self.frames[num_frame] if categ == category or category is None],
            [position.y for position, categ in self.frames[num_frame] if categ == category or category is None]
        )