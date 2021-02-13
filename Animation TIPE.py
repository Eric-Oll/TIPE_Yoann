# coding: utf-8

"""
CONSEILS :
> Créer un module dédié pour les routes qui expose uniquement la variable "roadmap" (liste des itinéraires)
 + créer une fonction pour la création du fond de carte
> Donner des noms de variable explicites qui auto-documente le code
"""
import logging

logging.basicConfig(level=logging.DEBUG, filename='./trace.log')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint
import random as rd

from road import Road
from vehicule import Vehicule
from landscape import create_landscape
from scenario import Scenario

# Paramètres de simulation
#-------------------------
NB_VEHICULE = 10        # Nombre de véhicule dans la simulation
MIN_TIME = 80           # Temps minimum entre les véhicules
MAX_DEPARTURE = 2000    # Heure maximum pour le départ des véhicules


### Un seul tour

# Section 1 : Initialisation

# 1.1 - Définitions:

# a) Limites du rond-point

r1, r2 = 15, 20

# b) Coordonnées
#n = rd.randint(0,2)                         # Sortie aléatoire (avec sortie i pour n == i-1)
rtraj = (r1+r2)/2                           # Rayon de la trajectoire

entree0 = Road(
    x_interval=(0,0),
    y_interval=(-42, rtraj*np.sin(-np.pi/2)),
    path_functions=(lambda t: t, lambda t: t)
    )

section0 = Road(
    x_interval=(-np.pi/2,0),
    y_interval=(-np.pi/2,0),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t:  rtraj*np.sin(t)),
    )

section1 = Road(
    x_interval=(0,np.pi/2),
    y_interval=(0,np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t:  rtraj*np.sin(t)),
    )

section2 = Road(
    x_interval=(np.pi/2,2*np.pi/2),
    y_interval=(np.pi/2,2*np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t:  rtraj*np.sin(t)),
    )

sortie0 = Road(
    x_interval=(rtraj, 42),
    y_interval=(0,0),
    path_functions=(lambda t: t, lambda t: t)
    )

sortie1 = Road(
    x_interval=(0, 0),
    y_interval=(rtraj,42),
    path_functions=(lambda t: t, lambda t: t)
    )

sortie2 = Road(
    x_interval=(-rtraj, -42),
    y_interval=(0,0),
    path_functions=(lambda t: t, lambda t: t)
    )

# itinairaires possibles
path1 = [entree0, section0, sortie0]
path2 = [entree0, section0, section1, sortie1]
path3 = [entree0, section0, section1, section2, sortie2]
roadmap = [path1, path2, path3]

#toto_car = Vehicule(roads=[path1, path2, path3][rd.randint(0,2)])
#yoyo_car = Vehicule(roads=[path1, path2, path3][rd.randint(0,2)])
#traffic = [toto_car, yoyo_car] # Liste de vehicule
traffic = [Vehicule(roads=roadmap[rd.randint(0,len(roadmap)-1)]) for x in range(NB_VEHICULE)]


# 1.2 - Création de la figure et du rond-point
# a) Création de la figure et paramétrages
fig, ax = plt.subplots()
ax.margins(0,0)

x_min, x_max, y_min, y_max = ax.axis('tight')
x_min, x_max, y_min, y_max = -39, 39, -29, 29
ax.set(xlim=(x_min, x_max), ylim=(y_min, y_max))

# Création du fond de carte
create_landscape(
    ax,                         # Zone grapgique
    r1,                         # Rayon interieur
    r2,                         # Rayon extérieur
    r = np.sqrt(63*r2**2/64)    # Constante choisie pour tronquer le cercle extérieur
    )


# Création de la ligne qui sera mise à jour au fur et à mesure
line, = ax.plot([],[], color='blue')
point, = ax.plot([], [], ls="none", marker="o")

# Gestion des limites de la fenêtre
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

# Définition de l'heure de départ des véhicules
departure_time = [x for x in range(0, MAX_DEPARTURE, MIN_TIME)] # On définit les heures de départ possibles
for vehicule in traffic: # Pour chaque véhicule on choisit une heure de départ
    vehicule.start(departure_time.pop(rd.randint(0,len(departure_time)-1))) #... au hasard et jamais la même heure

# Création du scénrio
movie = Scenario(traffic)


# Création de la fonction qui sera appelée à chaque nouvelle image de l'animation
def animate(k):
    coordonate = movie.get_data(k)
    logging.debug(f"Frame#{k} : {coordonate}")
    point.set_data(*coordonate)
    return point,

# Lancement de l'animation
ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=len(movie),
                              interval=20,
                              blit=True,
                              repeat = False)

plt.axis("equal")
plt.show()
