# coding: utf-8
"""
Module principale pour l'animation
"""
import logging

from parameters import * # Chargement des paramètres de simulation
from road_objects.road_item import RoadItem
from roadmaps.linear_road import LinearRoad
from roadmaps.linear_road_with_traffic_light import LinearRoadWithTrafficLight
from scenario import Scenario

import matplotlib.pyplot as plt
from matplotlib import animation, rc
import random as rd

from road_objects.vehicule import Vehicule
from roadmaps.traffic_circle import TrafficCircle

logging.BASIC_FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO,
                    # filemode='w', filename='./trace.log'
                    )

# Section 1 : Initialisation

# 1.2 - Création de la figure et du rond-point
# a) Création de la figure et paramétrages
fig, ax = plt.subplots()
ax.margins(0,0)
plt.axis("equal")

# Création de la carte
# simulation_map = TrafficCircle(ax)
# simulation_map = LinearRoad(ax)
simulation_map = LinearRoadWithTrafficLight(ax)

if SHOW_ROADS:
    for roadmap in simulation_map.roadmap:
        ax.plot(
            [pos.x for pos in roadmap],
            [pos.y for pos in roadmap],
            color='lightgray', linestyle='--'
        )

# Création de la liste de véhicules
traffic = [Vehicule(axe=ax, path=simulation_map.roadmap[rd.randint(0, len(simulation_map.roadmap) - 1)])
           for x in range(NB_VEHICULE)]


# Création de la ligne qui sera mise à jour au fur et à mesure
# line, = ax.plot([],[], color='blue')
point, = ax.plot([], [], ls="none", marker="o")


# points_list = []
# # for color in CATEG_COLORS:
# #     points_list.extend(ax.plot([],[], color=color, ls="none", marker="o"))
# for item in traffic:
#     # for line in item.get_components():
#     #     ax.add_line(line)
#     points_list.extend(item.get_components())
# text = ax.text(-20,2,"<texte>" )
# points_list.append(text)

# Génération de l'animation
departure_time = [x for x in range(0, MAX_DEPARTURE, MIN_TIME)] # On définit les heures de départ possibles
for i, vehicule in enumerate(traffic): # Pour chaque véhicule on choisit une heure de départ
    vehicule.start(departure_time.pop(rd.randint(0,len(departure_time)-1))) #... au hasard et jamais la même heure
    # section_size = int(len(departure_time)/len(traffic))
    # vehicule.start(departure_time[i*section_size:min((i+1)*section_size, len(departure_time))][rd.randint(0, section_size-1)])
    vehicule.speed = [1,2,3,4][rd.randint(0,3)]

# Création du scénrio
movie = Scenario(traffic, ax)

simulation_map.landscape()

ani = animation.FuncAnimation(fig=fig,
                              func=movie,
                              # fargs=points_list,
                              frames=movie.get_sequence(),
                              interval=FRAMES_INTERVAL,
                              # init_func=simulation_map.landscape,
                              blit=True,
                              repeat=False)
plt.show()

# ani.save('./video_TIPE.mp4')

