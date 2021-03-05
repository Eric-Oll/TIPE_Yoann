"""
Ce module regroupe la liste des paramètres de simulation

"""
import numpy as np

FLAG_REPORT = False      # Indicateur de création d'un report de données
SHOW_ROADS = False        # Indicateur de visualisation des routes

FRAMES_INTERVAL = 20    # Interval de temps entre 2 frames (ms)

NB_VEHICULE = 10       # Nombre de véhicules dans la simulation
MIN_TIME = 30           # Temps minimum entre les véhicules
MAX_DEPARTURE = 300    # Heure maximum pour le départ des véhicules

# Liste des couleurs par catégorie de vitesse
CATEG_COLORS = \
    ['red', 'orange', 'yellow', 'yellowgreen', 'limegreen', 'lime']

# Paramètres de vitesse des véhicules
MAX_SPEED = 5           # Vitesse maximum
MAX_SPEED_DOWN = 1    # %age max. de décélération
MAX_SPEED_UP = 0.5      # %age max. d'accélération
MIN_DISTANCE = 5      # distance minimal avec entre les RoadItem
SPEED_START = 1       # Vitesse de démarrage

# Fonction d'accélération maximum
# MAX_SPEED_UP_FUNC = lambda speed, distance: speed+speed*MAX_SPEED_UP
MAX_SPEED_UP_FUNC = lambda speed, distance: speed+0.1

# Fonction de décélération maximum
# MAX_SPEED_DOWN_FUNC = lambda speed, distance: speed-speed*MAX_SPEED_DOWN
MAX_SPEED_DOWN_FUNC = lambda speed, distance: speed-1

# Fonction de calcul de la distance
DISTANCE = lambda pos1, pos2: abs(pos1.x-pos2.x) + abs(pos1.y-pos2.y) # Norme 1
# DISTANCE = lambda pos1, pos2: np.sqrt((pos1.x-pos2.x)**2 + (pos1.y-pos2.y)**2) # Norme 2

# Distance entre deux positions
DISTANCE_POSITION = 0.05