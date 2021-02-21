"""
Ce module regroupe la liste des paramètres de simulation

"""

NB_VEHICULE = 5       # Nombre de véhicules dans la simulation
MIN_TIME = 10           # Temps minimum entre les véhicules
MAX_DEPARTURE = 200    # Heure maximum pour le départ des véhicules

# Liste des couleurs par catégorie de vitesse
CATEG_COLORS = \
    ['red', 'orange', 'yellow', 'yellowgreen', 'limegreen', 'lime']

# Paramètres de vitesse des véhicules
MAX_SPEED = 5           # Vitesse maximum
MAX_SPEED_DOWN = 0.1    # %age max. de décélération
MAX_SPEED_UP = 0.05      # %age max. d'accélération
MIN_DISTANCE = 10      # distance minimal avec entre les RoadItem
SPEED_START = 1       # Vitesse de démarrage

# Fonction d'accélération maximum
# MAX_SPEED_UP_FUNC = lambda speed, distance: speed+speed*MAX_SPEED_UP
MAX_SPEED_UP_FUNC = lambda speed, distance: speed+0.5

# Fonction de décélération maximum
# MAX_SPEED_DOWN_FUNC = lambda speed, distance: speed-speed*MAX_SPEED_DOWN
MAX_SPEED_DOWN_FUNC = lambda speed, distance: speed-0.5