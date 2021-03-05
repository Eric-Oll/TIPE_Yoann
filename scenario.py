"""
Ce module contient
- class Scenario => permet de calculer par anticipation la position des véhicules

"""
import logging
import pandas as pd
from itertools import chain
from parameters import FLAG_REPORT
from road_objects.road_item import RoadItem
from road_objects.traffic_light import TrafficLight

MAX_FRAMES = 10000   # Nombre maximum d'étape du scénario

class Scenario:
    """
    Calcule la position des véhicules avant l'animation

    """
    def __init__(self, traffic: list, axe):
        self._ax = axe              # Axes de matplotlib pour l'affichage
        self._traffic = traffic     # Liste des véhicules
        self._frames = list()       # liste des coordonnées pour le traffic pour une étape

        # Rapport de données
        self.report = pd.DataFrame(columns=['frame', 'parameter']+[vehicule.name for vehicule in self._traffic])

        # Obsolète  : self.create_frames()

        self._artists = list()
        for item in traffic:
            self._artists.extend(item.get_components())

        self.text = axe.text(0,2,"<texte>" )
        self._artists.append(self.text)
        # for color in CATEG_COLORS:
        #     self.points_list.extend(ax.plot([], [], color=color, ls="none", marker="o"))
        # text = ax.text(-20,2,"<texte>" )
        # self.points_list.append(text)

    def __len__(self):
        return len(self.frames)

    @property
    def artists(self):
        return self._artists

    @property
    def frames(self):
        return self._frames


    def __call__(self, frame, *args, **kwargs):
        """
                Fonction appelé pour l'affichage des Frames
        """
        print(f"{frame}", end="..")
        self.text.set_text(f"Frame {frame} => Nb vehicle running = {len([v for v in self._traffic if v.is_running])}")
        logging.debug(f"Points_list at #0 : {args}")

        if frame % 100 == 0:
            for trafficlight in [item for item in RoadItem.Get_Items() if isinstance(item, TrafficLight)]:
                trafficlight.set_passable(not trafficlight.passable)

        # Mise à jour de la vitesse des véhicule
        for vehicule in self._traffic:
            if vehicule.is_running:
                # logging.log(0, f"Frame #{frame} : Update Speed for {vehicule.name} ...")
                list_distance = []
                for item in [item for item in vehicule.Get_Items() if item.is_running and vehicule != item and not item.passable]:
                    d = vehicule.distance(item.next_position)
                    # logging.debug(
                    #     f"Frame #{frame} : compare with {item.name} / distance={d} (position={item.next_position}")
                    if d is not None:
                        list_distance.append(d)
                # logging.log(0, f"Frame #{frame} : List of distances = {list_distance}")
                # logging.log(0,
                #             f"Frame #{frame} : Update Speed for {vehicule.name} : distance with other {list_distance}")
                if len(list_distance) > 0:
                    vehicule.update_speed(min(list_distance))
                else:
                    vehicule.update_speed()

            arts = list()
            for item in RoadItem.Get_Items():
                arts.extend(item.get_plot(frame))

        # Collecte des données de reporting
        if FLAG_REPORT:
            # Statut
            self.report = self.report.append(dict(zip(report.columns,
                                            [frame, 'running'] + [vehicule.is_running for vehicule in
                                                                      self._traffic])),
                                   ignore_index=True)

            # Vitesse
            self.report = self.report.append(dict(zip(report.columns,
                                            [frame, 'speed'] + [vehicule.speed for vehicule in self._traffic])),
                                   ignore_index=True)

            # Position
            self.report = self.report.append(dict(zip(report.columns,
                                            [frame, 'position'] + [(vehicule.position.x, vehicule.position.y)
                                                                       if vehicule.position else None
                                                                       for vehicule in self._traffic])),
                                   ignore_index=True)

        # ... Fin collecte reporting

        # self.artists.clear()
        # for item in RoadItem.Get_Items():
        #     item.forward(frame)
        #     if item.is_running:
        #         self.artists.extend(item.get_plot(ax=self._ax))

        # self.artists = [item for item in self.artists if item is not None]
        logging.debug(f"""Frame #{frame} : Liste des artists -> {repr(self.artists)}""")
        logging.debug(f"""Frame #{frame} : Liste des points_list -> {repr(args)}""")

        arts.append(self.text)
        return arts
        # return chain([self.text], *[item.get_plot() for item in RoadItem.Get_Items() if item.is_running])
        # return [item for item in self.artists if item is not None]
        # return args if not None else self.artists

    @property
    def frame(self):
        return self._frames

    def get_sequence(self):
        num_frame = 0
        while not all([vehicule.is_ended for vehicule in self._traffic]) and num_frame < MAX_FRAMES:
            logging.debug(f"Scenario.get_sequence : Nouveau n° de frame : {num_frame}")
            yield num_frame
            num_frame += 1
        print("End of movie.")

        # Génération du fichier de réporting
        if FLAG_REPORT:
            report.to_csv('./report_simulation.csv', sep=';', index=None)



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
        report = pd.DataFrame(columns=['frame', 'parameter']+[vehicule.name for vehicule in self._traffic])

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
            print(f"{num_frame}",end="..")

            # Mise à jour de la vitesse des véhicule
            for vehicule in self._traffic:
                if vehicule.is_running:
                    logging.log(0, f"Frame #{num_frame} : Update Speed for {vehicule.name} ...")
                    list_distance = []
                    for item in [item for item in vehicule.Get_Items() if item.is_running and vehicule != item]:
                        d = vehicule.distance(item.next_position)
                        logging.debug(f"Frame #{num_frame} : compare with {item.name} / distance={d} (position={item.next_position}")
                        if d is not None:
                            list_distance.append(d)
                    logging.log(0, f"Frame #{num_frame} : List of distances = {list_distance}")
                    logging.log(0, f"Frame #{num_frame} : Update Speed for {vehicule.name} : distance with other {list_distance}")
                    if len(list_distance) > 0:
                        vehicule.update_speed(min(list_distance))
                    else:
                        vehicule.update_speed()

            # Collecte des données de reporting
            if FLAG_REPORT:
                # Statut
                report = report.append(dict(zip(report.columns,
                                                [num_frame, 'running'] + [vehicule.is_running for vehicule in self._traffic])),
                                       ignore_index=True)

                # Vitesse
                report = report.append(dict(zip(report.columns,
                                                [num_frame, 'speed'] + [vehicule.speed for vehicule in self._traffic])),
                                       ignore_index=True)

                # Position
                report = report.append(dict(zip(report.columns,
                                                [num_frame, 'position'] + [(vehicule.position.x, vehicule.position.y)
                                                                           if vehicule.position else None
                                                                           for vehicule in self._traffic])),
                                       ignore_index=True)


            # ... Fin collecte reporting

            self.add_frame({'position' :[(vehicule.get_position(num_frame), vehicule.category) for vehicule in self._traffic],
                            'state': [(vehicule.name, vehicule.is_running) for vehicule in self._traffic],
                            })
            num_frame += 1      # On passe à la frame suivante

        # Génération du fichier de réporting
        if FLAG_REPORT:
            report.to_csv('./report_simulation.csv', sep=';', index=None)


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

    def get_state(self, num_frame:int)->list:
        """
        Retourne l'état des véhicules pour la frame <num_frame>
        :return: [(name, state), ...]
        """
        return self.frame[num_frame]['state']