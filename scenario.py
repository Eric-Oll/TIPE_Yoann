"""
Ce module contient
- class Scenario => permet de calculer par anticipation la position des véhicules

"""
import logging
import pandas as pd
from itertools import chain
from parameters import FLAG_REPORT, SHOW_FRAME
from road_objects.road_item import RoadItem
from road_objects.traffic_light import TrafficLight

MAX_FRAMES = 10000   # Nombre maximum d'étape du scénario

class Scenario:
    """
    Calcule la position des véhicules pour l'animation
    """

    def __init__(self, traffic: list, axe):
        self._ax = axe              # Axes de matplotlib pour l'affichage
        self._traffic = traffic     # Liste des véhicules

        # Rapport de données
        self.report = pd.DataFrame(columns=['frame', 'parameter']+[vehicule.name for vehicule in self._traffic])

        if SHOW_FRAME:
            self.text = axe.text(axe.get_xlim()[0],axe.get_ylim()[1],"<texte>", ha='left', va='top' )

    def __call__(self, frame, *args, **kwargs):
        """
                Fonction appelé pour l'affichage des Frames
        """
        if SHOW_FRAME:
            self.text.set_text(f"Frame {frame}\n=> Nb vehicle running = {len([v for v in self._traffic if v.is_running])}")

        # Mise à jour de la vitesse des véhicule
        for vehicule in self._traffic:
            if vehicule.is_running:
                list_distance = {}
                for item in [item for item in vehicule.Get_Items() if item.is_running and vehicule != item and not item.passable]:
                    d = vehicule.distance(item.next_position)
                    if d is not None:
                        list_distance[item.name] = d
                logging.debug(f"Frame #{frame} : List of distances for {vehicule.name} = {list_distance}")
                if len(list_distance) > 0:
                    vehicule.update_speed(min(list_distance.values()))
                else:
                    vehicule.update_speed()

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

        # Création de la liste des objets graphique à mettre à jour
        arts = list()
        for item in RoadItem.Get_Items():
            arts.extend(item.get_plot(frame))

        if SHOW_FRAME:
            arts.append(self.text)  # Mise à jour de l'affichage du numéro de frame

        return arts # On retourne la liste des objets graphique à mettre à jour pour la frame

    def get_sequence(self):
        """
        Génère un numéro de frame ...
        ... et à la fin crée le fichier de reporting si le flag FLAG_REPORT est activé
        """

        num_frame = 0
        while not all([vehicule.is_ended for vehicule in self._traffic]) and num_frame < MAX_FRAMES:
            logging.debug(f"\nScenario.get_sequence : Nouveau n° de frame : {num_frame}")
            yield num_frame
            num_frame += 1
        print("End of movie.")

        # Génération du fichier de réporting
        if FLAG_REPORT:
            report.to_csv('./report_simulation.csv', sep=';', index=None)


