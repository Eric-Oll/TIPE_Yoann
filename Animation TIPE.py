# coding: utf-8
"""
Module principale pour l'animation
"""
import logging

from parameters import * # Chargement des paramètres de simulation
from roadmaps.linear_road import LinearRoad
from scenario import Scenario

import matplotlib.pyplot as plt
from matplotlib import animation, rc
import random as rd

from road_objects.vehicule import Vehicule
from roadmaps.traffic_circle import TrafficCircle

logging.basicConfig(level=logging.DEBUG,
                    filemode='w', filename='./trace.log'
                    )

# Section 1 : Initialisation

# 1.2 - Création de la figure et du rond-point
# a) Création de la figure et paramétrages
fig, ax = plt.subplots()
ax.margins(0,0)

# x_min, x_max, y_min, y_max = ax.axis('tight')
# x_min, x_max, y_min, y_max = -39, 39, -29, 29
# ax.set(xlim=(x_min, x_max), ylim=(y_min, y_max))

# Création de la carte
# simulation_map = TrafficCircle(ax)
simulation_map = LinearRoad(ax)

# Création de la liste de véhicules
traffic = [Vehicule(path=simulation_map.roadmap[rd.randint(0, len(simulation_map.roadmap) - 1)])
           for x in range(NB_VEHICULE)]


# Création de la ligne qui sera mise à jour au fur et à mesure
# line, = ax.plot([],[], color='blue')
point, = ax.plot([], [], ls="none", marker="o")


points_list = []
for color in CATEG_COLORS:
    points_list.extend(ax.plot([],[], color=color, ls="none", marker="o"))


# Gestion des limites de la fenêtre
# ax.set_xlim([-2, 2])
# ax.set_ylim([-2, 2])

# Création de la fonction qui sera appelée à chaque nouvelle image de l'animation
def animate(k):
    # logging.debug(f"Frame {k}")

    # point.set_data(*movie.get_data(k))
    # return point,
    for categ in range(len(CATEG_COLORS)):
        x_series, y_series = movie.get_data(k, categ)
        logging.debug(f"Frame : {k}, Categ.{categ} :")
        if len(x_series) != 0:
            # logging.debug(f"... : X={x_series}")
            # logging.debug(f"... : Y={y_series}")
            points_list[categ].set_data(x_series, y_series)
        else:
            logging.debug(f"... : pas de données")

    return points_list

# Génération de l'animation
departure_time = [x for x in range(0, MAX_DEPARTURE, MIN_TIME)] # On définit les heures de départ possibles
for vehicule in traffic: # Pour chaque véhicule on choisit une heure de départ
    vehicule.start(departure_time.pop(rd.randint(0,len(departure_time)-1))) #... au hasard et jamais la même heure
    vehicule.speed = [1,2,3,4][rd.randint(0,3)]

# Création du scénrio
movie = Scenario(traffic)

for art in simulation_map.landscape():
    art

ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=len(movie),
                              interval=FRAMES_INTERVAL,
                              # init_func=simulation_map.landscape,
                              blit=True,
                              repeat=False)

plt.axis("equal")

# ani.save('./video_TIPE.mp4')
plt.show()
