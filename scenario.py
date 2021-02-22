"""
Ce module contient
- class Scenario => permet de calculer par anticipation la position des véhicules

"""
import logging
import pandas as pd
from parameters import FLAG_REPORT

MAX_FRAMES = 10000   # Nombre maximum d'étape du scénario

class Scenario:
    """
    Calcule la position des véhicules avant l'animation

    """
    def __init__(self, traffic: list):
        self._traffic = traffic     # Liste des véhicules
        self._frames = list()       # liste des coordonnées pour le traffic pour une étape
        self.create_frames()

    def __len__(self):
        return len(self.frame)

    @property
    def frame(self):
        return self._frames

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
            [position.x for position, categ in self.frame[num_frame]['position'] if categ==category or category is None],
            [position.y for position, categ in self.frame[num_frame]['position'] if categ==category or category is None]
        )

    def get_state(self, num_frame:int)->list:
        """
        Retourne l'état des véhicules pour la frame <num_frame>
        :return: [(name, state), ...]
        """
        return self.frame[num_frame]['state']