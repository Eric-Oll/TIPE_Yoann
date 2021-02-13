# coding: utf-8

"""
CONSEILS :
> Créer un module dédié pour les routes qui expose uniquement la variable "roadmap" (liste des itinéraires)
 + créer une fonction pour la création du fond de carte
> Donner des noms de variable explicites qui auto-documente le code
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint
import random as rd

# Paramètres de simulation
#-------------------------
NB_VEHICULE = 20        # Nombre de véhicule dans la simulation
MIN_TIME = 30           # Temps minimum entre les véhicules
MAX_DEPARTURE = 2000    # Heure maximum pour le départ des véhicules

# Définition des classes Road et Vehicule
# ---------------------------------------
class Road(object):
    """
    Définit la fonction de calcul de la trajectoire entre deux positions.
    """

    def __init__(self, x_interval, y_interval, path_functions, step=100):
        """
        x_interval : Interval de calcul (x_start, x_end)
        y_interval : Interval de calcul (y_start, y_end)
        path_functions : fonctions paramétriques (x_func, y_func)
            de calcul de la trajectoire entre les deux positions
        """
        self.x_interval = x_interval
        self.y_interval = y_interval
        self.path_functions = path_functions
        self.step = step
        self.setup_path()

    def setup_path(self):
        """
        Calcul les Coordonnées de la routes
        """
        self.path = [(x,y) \
            for x, y in zip(
                self.path_functions[0](np.linspace(*self.x_interval, self.step)),
                self.path_functions[1](np.linspace(*self.y_interval, self.step))
                )]


class Vehicule(object):
    """
    Regroupe les routes  de son itinairaire
    et définit la position du véhicule dans le temps
    """

    def __init__(self, roads=None):
        self.init_time = 0
        self.path = [] # Liste des routes à prendre par le Vehicule
        if roads is not None:
            self.add_path(roads)

    @property
    def length(self):
        return len(self.path)

    @property
    def travel_time(self):
        return self.init_time + self.length

    def add_path(self, roads:list):
        """
        Ajoute une route à l'itinairaire
        """
        for road in roads:
            self.path.extend(road.path)

    def start(self, init_time):
        """
        Définit le moment du départ
        => permet un décalage dans la lecture des positions
        """
        self.init_time = init_time

    def get_position(self, current_time):
        """
        Retourne la position (x,y) du Vehicule
        """
        real_time = current_time-self.init_time
        return (None, None) if real_time<0 or real_time>= len(self.path) else self.path[real_time]


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
    step=100
    )

section1 = Road(
    x_interval=(0,np.pi/2),
    y_interval=(0,np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t:  rtraj*np.sin(t)),
    step=100
    )

section2 = Road(
    x_interval=(np.pi/2,2*np.pi/2),
    y_interval=(np.pi/2,2*np.pi/2),
    path_functions=(lambda t: rtraj*np.cos(t), lambda t:  rtraj*np.sin(t)),
    step=100
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

#t = np.linspace(-np.pi/2, n*np.pi/2, (n+1)*100) # Paramètres pour la position de la voiture
                                                # (n+1)*100 -> pour avoir vitesse constante du point
#x = rtraj*np.cos(t)                             # Abscisses de la voiture dans le rond-point
#y = rtraj*np.sin(t)                             # Ordonnées de la voiture dans le rond-point

#if n==0:                                        # Coordonnées de la voiture en sortie 1
#    xsortie1 = np.linspace(rtraj, 42, 100)
#    ysortie1 = np.linspace(0,0,100)
#    x = np.concatenate((x,xsortie1), axis = 0)
#    y = np.concatenate((y,ysortie1), axis = 0)
#elif n==1:                                      # Coordonnées de la voiture en sortie 2
#    xsortie2 = np.linspace(0, 0, 100)
#    ysortie2 = np.linspace(rtraj,42,100)
#    x = np.concatenate((x,xsortie2), axis = 0)
#    y = np.concatenate((y,ysortie2), axis = 0)
#else:                                           # Coordonnées de la voiture en sortie 3
#    xsortie3 = np.linspace(-rtraj, -42, 100)
#    ysortie3 = np.linspace(0,0,100)
#    x = np.concatenate((x,xsortie3), axis = 0)
#    y = np.concatenate((y,ysortie3), axis = 0)

r = np.sqrt(63*r2**2/64)                    # Constante choisie pour tronquer le cercle extérieur

# 1.2 - Création de la figure et du rond-point

# a) Création de la figure et paramétrages

fig, ax = plt.subplots()
ax.margins(0,0)
x_min, x_max, y_min, y_max = ax.axis('tight')
x_min, x_max, y_min, y_max = -39, 39, -29, 29
ax.set(xlim=(x_min, x_max), ylim=(y_min, y_max))

# b) Création du rond-point

def f1(x,r): # Création de la partie positive du cercle extérieur, tronqué
    y=x**2-63*r/64
    return np.sqrt(np.sqrt(y/abs(y))*(r**2*(np.sqrt((abs(abs(x)-r/8))/(abs(x)-r/8)))-(x**2)))

def f2(x,r): # Création de la partie négative du cercle extérieur, tronqué
    y=x**2-63*r/64
    return -np.sqrt(np.sqrt(y/abs(y))*(r**2*(np.sqrt((abs(abs(x)-r/8))/(abs(x)-r/8)))-(x**2)))

# c) Création des routes liées au rond-point
f3 = lambda x: -r/8
f4 = lambda x: r/8

# Abscisses
X1=np.linspace(0,r1,100) # Pour la partie positive du cercle intérieur
X2=np.linspace(0,-r1,100) # Pour la partie négative du cercle intérieur
X3 = np.linspace(-r,r,100) # Pour la partie positive du cercle extérieur, tronqué
X4 = np.linspace(-r,r,100) # Pour la partie négative du cercle extérieur, tronqué
X5 = np.linspace(-2*r,-r,100) # Pour la route ouest
X6 = np.linspace(r,2*r,100) # Pour la route est

# Ordonnées

Y1 = [np.sqrt(r1**2-x**2) for x in X1] # Pour la partie positive du cercle intérieur
Y2 = [-np.sqrt(r1**2-x**2) for x in X2] # Pour la partie négative du cercle intérieur
Y3 = [f1(x,r2) for x in X3] # Pour la partie positive du cercle extérieur, tronqué
Y4 = [f2(x,r2) for x in X4] # Pour la partie négative du cercle extérieur, tronqué
Y5 = [f3(x) for x in X5] # Pour la route ouest
Y6 = [f4(x) for x in X6] # Pour la route est

# Tracés des courbes dans un même graphe

plt.axis("equal")
ax.plot(X1,Y1,'b') # Cercle intérieur
ax.plot(X2,Y1,'b') # Cercle intérieur
ax.plot(X1,Y2,'b') # Cercle intérieur
ax.plot(X2,Y2,'b') # Cercle intérieur
ax.plot(X3,Y3,'b') # Cercle extérieur, tronqué
ax.plot(X4,Y3,'b') # Cercle extérieur, tronqué
ax.plot(X3,Y4,'b') # Cercle extérieur, tronqué
ax.plot(X4,Y4,'b') # Cercle extérieur, tronqué
ax.plot(X5,Y5,'b') # Route ouest
ax.plot(X6,Y5,'b') # Route est
ax.plot(X5,Y6,'b') # Route ouest
ax.plot(X6,Y6,'b') # Route est
ax.plot([-r/5, -r/5], [y_min, min(Y4)], 'b') # Route sud
ax.plot([-r/5, -r/5], [max(Y3), y_max], 'b') # Route nord
ax.plot([r/5, r/5], [y_min, min(Y4)], 'b') # Route sud
ax.plot([r/5, r/5], [max(Y3), y_max], 'b') # Route nord

# Création de la ligne qui sera mise à jour au fur et à mesure

line, = ax.plot([],[], color='blue')
point, = ax.plot([], [], ls="none", marker="o")
# Gestion des limites de la fenêtre

ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

# Création de la fonction qui sera appelée à chaque nouvelle image de l'animation

def animate(k):
    #i = min(k, x.size)
    #line.set_data(x[:i], y[:i]) #pour avoir le chemin parcouru
    #point.set_data([x[i], x[max(0,i-10)]], [y[i], y[max(0,i-10)]])
    positions_list = [x.get_position(k) for x in traffic]
    point.set_data([x for x,y in positions_list], [y for x,y in positions_list])
    return line, point

# Génération de l'animation
departure_time = [x for x in range(0, MAX_DEPARTURE, MIN_TIME)] # On définit les heures de départ possibles
for vehicule in traffic: # Pour chaque véhicule on choisit une heure de départ
    vehicule.start(departure_time.pop(rd.randint(0,len(departure_time)-1))) #... au hasard et jamais la même heure
#toto_car.start(0)
#yoyo_car.start(10)

ani = animation.FuncAnimation(fig=fig, func=animate, frames=range(max(vehicule.travel_time for vehicule in traffic)), interval=20, blit=True, repeat = False)
#ani = animation.FuncAnimation(fig=fig, func=animate, frames=range(x.size), interval=20, blit=True, repeat = True)

plt.axis("equal")
plt.show()
