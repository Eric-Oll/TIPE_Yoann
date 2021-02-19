# coding: utf-8
"""
Carte d'un rond-point


Création du fond de carte
"""
import numpy as np
from roadmaps.path import Path
from roadmaps.road import Road


# __ALL__ = [
#     landscape, # Fond de route
#     roadmap,    # Itinéraires pour les véhicules
# ]
r1 = 15     # Rayon interieur
r2 = 20     # Rayon extérieur

# b) Coordonnées
#n = rd.randint(0,2)                         # Sortie aléatoire (avec sortie i pour n == i-1)
rtraj = (r1+r2)/2                            # Rayon de la trajectoire
r = np.sqrt(63*r2**2/64)                     # Constante choisie pour tronquer le cercle extérieur

#################################################################################################
# Création des portions de routes
#################################################################################################
# ... Les entrées de rond-point
# -----------------------------
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

# ... Les sections de rond-points
# --------------------------------
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

# ... Les sorties de rond-point
# ------------------------------
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

# ... Les jointions entre les sections de rond-point
# --------------------------------------------------
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
# ----------------------
path01 = Path(entree0, section0, sortie1)
path02 = Path(entree0, section0, jonction1, section1, sortie2)
path03 = Path(entree0, section0, jonction1, section1, jonction2, section2, sortie3)
path12 = Path(entree1, section1, sortie2)
path13 = Path(entree1, section1, jonction2, section2, sortie3)
path10 = Path(entree1, section1, jonction2, section2, jonction3, section3, sortie0)
path23 = Path(entree2, section2, sortie3)
path20 = Path(entree2, section2, jonction3, section3, sortie0)
path21 = Path(entree2, section2, jonction3, section3, jonction0, section0, sortie1)
path30 = Path(entree3, section3, sortie0)
path31 = Path(entree3, section3, jonction0, section0, sortie1)
path32 = Path(entree3, section3, jonction0, section0, jonction1, section1, sortie2)

# Liste des itinéraires
#----------------------
roadmap = [path01, path02, path03,
           path12, path13, path10,
           path23, path20, path21,
           path30, path31, path32]

# Fond d'écran
def f1(x,r): # Création de la partie positive du cercle extérieur, tronqué
    y = x**2-63*r/64
    return np.sqrt(np.sqrt(y/abs(y))*(r**2*(np.sqrt((abs(abs(x)-r/8))/(abs(x)-r/8)))-(x**2)))

def f2(x,r): # Création de la partie négative du cercle extérieur, tronqué
    y = x**2-63*r/64
    return -np.sqrt(np.sqrt(y/abs(y))*(r**2*(np.sqrt((abs(abs(x)-r/8))/(abs(x)-r/8)))-(x**2)))

# TODO : Transformer landscape en fonction d'init. pour l'animation
def landscape(ax):
    """
    ax : objet Axes (matplotlib)
    r1 : rayon du rond point interieur
    r2 : rayon du rond point extérieur
    r : constante pour tronquer le rond point extérieur
    """
    # Limite de la zone graphique
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    # c) Création des routes liées au rond-point
    f3 = lambda x: -r/8
    f4 = lambda x: r/8

    # Abscisses
    X1 = np.linspace(0,r1,100) # Pour la partie positive du cercle intérieur
    X2 = np.linspace(0,-r1,100) # Pour la partie négative du cercle intérieur
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
