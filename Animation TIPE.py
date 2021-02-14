# coding: utf-8

"""
CONSEILS :
> Créer un module dédié pour les routes qui expose uniquement la variable "roadmap" (liste des itinéraires)
 + créer une fonction pour la création du fond de carte
> Donner des noms de variable explicites qui auto-documente le code
"""
import logging

from scenario import Scenario

logging.basicConfig(level=logging.INFO)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint
import random as rd

from road import Road
from vehicule import Vehicule
from landscape import create_landscape


# Paramètres de simulation
#-------------------------
NB_VEHICULE = 100        # Nombre de véhicules dans la simulation
MIN_TIME = 30           # Temps minimum entre les véhicules
MAX_DEPARTURE = 3000    # Heure maximum pour le départ des véhicules


### Un seul tour

# Section 1 : Initialisation

# 1.1 - Définitions :

# a) Limites du rond-point

r1, r2 = 15, 20

# b) Coordonnées
#n = rd.randint(0,2)                         # Sortie aléatoire (avec sortie i pour n == i-1)
rtraj = (r1+r2)/2                            # Rayon de la trajectoire
r = np.sqrt(63*r2**2/64)

entree0 = Road(
    x_interval=(r/7,r/7),
    y_interval=(-42,-rtraj),
    path_functions=(lambda t: t, lambda t: t)
    )

entree1 = Road(
    x_interval=(42,rtraj),
    y_interval=(r/24,r/24),
    path_functions=(lambda t: t, lambda t: t)
    )

entree2 = Road(
    x_interval=(-r/7,-r/7),
    y_interval=(42,rtraj),
    path_functions=(lambda t: t, lambda t: t)
    )

entree3 = Road(
    x_interval=(-42,-rtraj),
    y_interval=(-r/24,-r/24),
    path_functions=(lambda t: t, lambda t: t)
    )

section0 = Road(
    x_interval=(np.arccos((r/7)/rtraj),0),
    y_interval=(-np.pi/2,np.arcsin(-(r/24)/rtraj)),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
    step=100
    )

section1 = Road(
    x_interval=(0,np.arccos((r/7)/rtraj)),
    y_interval=(np.arcsin((r/24)/rtraj),np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
    step=100
    )

section2 = Road(
    x_interval=(np.arccos(-(r/7)/rtraj),np.pi),
    y_interval=(np.pi/2,np.arcsin((r/24)/rtraj)),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
    step=100
    )

section3 = Road(
    x_interval=(np.pi,np.arccos(-(r/7)/rtraj)),
    y_interval=(np.arcsin(-(r/24)/rtraj),-np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
    step=100
    )

sortie0 = Road(
    x_interval=(-r/7,-r/7),
    y_interval=(-rtraj,-42),
    path_functions=(lambda t: t, lambda t: t)
    )

sortie1 = Road(
    x_interval=(rtraj, 42),
    y_interval=(-r/24,-r/24),
    path_functions=(lambda t: t, lambda t: t)
    )

sortie2 = Road(
    x_interval=(r/7,r/7),
    y_interval=(rtraj,42),
    path_functions=(lambda t: t, lambda t: t)
    )

sortie3 = Road(
    x_interval=(-rtraj, -42),
    y_interval=(r/24,r/24),
    path_functions=(lambda t: t, lambda t: t)
    )

jonction0 = Road(
    x_interval=(np.arccos(-(r/7)/rtraj),np.arccos((r/7)/rtraj)),
    y_interval=(-np.pi/2,-np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
    step=25
    )

jonction1 = Road(
    x_interval=(0,0),
    y_interval=(np.arcsin(-(r/24)/rtraj),np.arcsin((r/24)/rtraj)),
    path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
    step=9
    )

jonction2 = Road(
    x_interval=(np.arccos((r/7)/rtraj),np.arccos(-(r/7)/rtraj)),
    y_interval=(np.pi/2,np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
    step=25
    )

jonction3 = Road(
    x_interval=(np.pi,np.pi),
    y_interval=(np.arcsin((r/24)/rtraj),np.arcsin(-(r/24)/rtraj)),
    path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
    step=9
    )

# Itinéraires possibles
path01 = [entree0, section0, sortie1]
path02 = [entree0, section0, jonction1, section1, sortie2]
path03 = [entree0, section0, jonction1, section1, jonction2, section2, sortie3]
path12 = [entree1, section1, sortie2]
path13 = [entree1, section1, jonction2, section2, sortie3]
path10 = [entree1, section1, jonction2, section2, jonction3, section3, sortie0]
path23 = [entree2, section2, sortie3]
path20 = [entree2, section2, jonction3, section3, sortie0]
path21 = [entree2, section2, jonction3, section3, jonction0, section0, sortie1]
path30 = [entree3, section3, sortie0]
path31 = [entree3, section3, jonction0, section0, sortie1]
path32 = [entree3, section3, jonction0, section0, jonction1, section1, sortie2]

roadmap = [path01, path02, path03,
           path12, path13, path10,
           path23, path20, path21,
           path30, path31, path32]

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
    r=np.sqrt(63*r2**2/64)    # Constante choisie pour tronquer le cercle extérieur
    )


# Création de la ligne qui sera mise à jour au fur et à mesure
line, = ax.plot([],[], color='blue')
point, = ax.plot([], [], ls="none", marker="o")

# Gestion des limites de la fenêtre
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

# Création de la fonction qui sera appelée à chaque nouvelle image de l'animation
def animate(k):
    # logging.debug(f"Frame {k}")


    #positions_list = [x.get_position(k) for x in traffic]
    #point.set_data([x for x,y in positions_list], [y for x,y in positions_list])
    point.set_data(*movie.get_data(k))
    return point,

# Génération de l'animation
departure_time = [x for x in range(0, MAX_DEPARTURE, MIN_TIME)] # On définit les heures de départ possibles
for vehicule in traffic: # Pour chaque véhicule on choisit une heure de départ
    vehicule.start(departure_time.pop(rd.randint(0,len(departure_time)-1))) #... au hasard et jamais la même heure
#toto_car.start(0)
#yoyo_car.start(10)

# Création du scénrio
movie = Scenario(traffic)

ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=len(movie),
                              interval=20,
                              blit=True,
                              repeat=False)
#ani = animation.FuncAnimation(fig=fig, func=animate, frames=range(x.size), interval=20, blit=True, repeat = True)

plt.axis("equal")

plt.show()
