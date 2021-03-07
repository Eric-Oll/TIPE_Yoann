# coding: utf-8
"""
Module principale pour l'animation
"""
import logging

from parameters import * # Chargement des paramètres de simulation
from road_objects.road_item import RoadItem
from roadmaps.linear_road import LinearRoad
from roadmaps.linear_road_with_traffic_light import LinearRoadWithTrafficLight
from roadmaps.map import Map
from scenario import Scenario

import matplotlib.pyplot as plt
from matplotlib import animation, rc
import random as rd

from road_objects.vehicule import Vehicule
from roadmaps.traffic_circle import TrafficCircle

logging.BASIC_FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO,
                    # filemode='w', filename='./trace.log',
                    format="%(msg)s"
                    )

def run(working_map:Map):
    """
    La fonction 'run' lance l'animation sur la Map passé en paramètre
    :parameters map: Classe Map correspondant à la carte sur laquelle faire l'animation
    """
    # Création du contexte graphique
    fig, ax = plt.subplots()
    plt.ion()
    ax.margins(0,0)
    ax.axis("equal")

    # Création de la carte
    simulation_map = working_map(ax)    # Création de la carte

    # Option d'affage de la route (voie des véhicules)
    if SHOW_ROADS:
        for roadmap in simulation_map.roadmap:
            ax.plot(
                [pos.x for pos in roadmap],
                [pos.y for pos in roadmap],
                color='lightgray', linestyle='--'   # Affiche en pointillé gris clair
            )

    # Création de la liste de véhicules
    traffic = [Vehicule(axe=ax, path=simulation_map.roadmap[rd.randint(0, len(simulation_map.roadmap) - 1)])
               for x in range(NB_VEHICULE)]

    # Génération de l'animation
    departure_time = [x for x in range(0, MAX_DEPARTURE, MIN_TIME)] # On définit les heures de départ possibles
    for i, vehicule in enumerate(traffic): # Pour chaque véhicule ...
        # ... on choisit une heure de départ au hasard et jamais la même heure
        vehicule.start(departure_time.pop(rd.randint(0,len(departure_time)-1)))
        # ... On choisie au hasard une vitesse initiale de véhicule
        vehicule.speed = [1,2,3,4][rd.randint(0,3)]

    # Création du film (instantiation du scénario)
    movie = Scenario(traffic, ax)

    # Affichage du paysage
    simulation_map.landscape()

    # Lancement de l'animation
    ani = animation.FuncAnimation(fig=fig,
                                  func=movie,
                                  frames=movie.get_sequence(),
                                  interval=FRAMES_INTERVAL,
                                  blit=True,
                                  save_count=2000,      # Nombre de frame tampon (calculé par avance
                                  )

    #ani.save('./video_TIPE.mp4', fps=30)
    plt.show(True)
    return ani

if __name__ == '__main__':
    run(TrafficCircle)

