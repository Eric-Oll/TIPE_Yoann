# coding: utf-8
"""
Carte d'un rond-point

"""
import logging

import numpy as np
from roadmaps.map import Map
from roadmaps.path import Path
from roadmaps.road import Road



class TrafficCircle(Map):
    RAYON_INTERIEUR = 15  # Rayon interieur
    RAYON_EXTERIEUR = 20  # Rayon extérieur
    r = np.sqrt(63 * RAYON_EXTERIEUR ** 2 / 64)  # Constante choisie pour tronquer le cercle extérieur

    def __init__(self, axe):
        super(TrafficCircle, self).__init__(axe=axe)
        self.init_graphic()
        self.init_roads()


    def init_roads(self):
        """
        Construction des routes
        """
        rtraj = (self.RAYON_INTERIEUR + self.RAYON_EXTERIEUR) / 2                            # Rayon de la trajectoire
        r = TrafficCircle.r
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
            step=500
            )

        section1 = Road(
            x_interval=(0,np.arccos((r/7)/rtraj)),
            y_interval=(np.arcsin((r/24)/rtraj),np.pi/2),
            path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
            step=500
            )

        section2 = Road(
            x_interval=(np.arccos(-(r/7)/rtraj),np.pi),
            y_interval=(np.pi/2,np.arcsin((r/24)/rtraj)),
            path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
            step=500
            )

        section3 = Road(
            x_interval=(np.pi,np.arccos(-(r/7)/rtraj)),
            y_interval=(np.arcsin(-(r/24)/rtraj),-np.pi/2),
            path_functions=(lambda t: rtraj*np.cos(t), lambda t: rtraj*np.sin(t)),
            step=500
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
            step=125
            )

        jonction1 = Road(
            x_interval=(0,0),
            y_interval=(np.arcsin(-(r/24)/rtraj),np.arcsin((r/24)/rtraj)),
            path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
            step=50
            )

        jonction2 = Road(
            x_interval=(np.arccos((r/7)/rtraj),np.arccos(-(r/7)/rtraj)),
            y_interval=(np.pi/2,np.pi/2),
            path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
            step=125
            )

        jonction3 = Road(
            x_interval=(np.pi,np.pi),
            y_interval=(np.arcsin((r/24)/rtraj),np.arcsin(-(r/24)/rtraj)),
            path_functions=(lambda t: rtraj*np.cos(t),lambda t: rtraj*np.sin(t)),
            step=50
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
        self._roadmap = [path01, path02, path03,
                         path12, path13, path10,
                         path23, path20, path21,
                         path30, path31, path32]

    # Fond d'écran
    def landscape(self):
        """
        r1 : rayon du rond point interieur
        r2 : rayon du rond point extérieur
        r : constante pour tronquer le rond point extérieur
        """
        r = TrafficCircle.r
        r1 = TrafficCircle.RAYON_INTERIEUR
        r2 = TrafficCircle.RAYON_EXTERIEUR

        # TODO : Revoir la fonction f1 pour qu'il n'y ait pas le message d'erreur
        def f1(x, r):  # Création de la partie positive du cercle extérieur, tronqué
            y = x ** 2 - 63 * r / 64
            Y = y / abs(y)
            X = (abs(abs(x) - r / 8)) / (abs(x) - r / 8)
            if Y < 0 or X < 0:
                # print(f"f1({x},{r}) => Y={Y}, X={X}")
                return np.nan
            elif np.sqrt(Y) * (r ** 2 * np.sqrt(X) - (x ** 2)) < 0:
                # print(f"f1({x},{r}) => np.sqrt(Y)*(r**2*np.sqrt(X)-(x**2))={np.sqrt(Y)*(r**2*np.sqrt(X)-(x**2))}")
                return np.nan

            value = np.sqrt(np.sqrt(Y) * (r ** 2 * np.sqrt(X) - (x ** 2)))
            return value

        f2 = lambda x, r: -f1(x, r)

        # Limite de la zone graphique
        x_min, x_max = self._ax.get_xlim()
        y_min, y_max = self._ax.get_ylim()

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
        artists = []
        artists.extend(self._ax.plot(X1,Y1,'b')) # Cercle intérieur
        artists.extend(self._ax.plot(X2,Y1,'b')) # Cercle intérieur
        artists.extend(self._ax.plot(X1,Y2,'b')) # Cercle intérieur
        artists.extend(self._ax.plot(X2,Y2,'b')) # Cercle intérieur
        artists.extend(self._ax.plot(X3,Y3,'b')) # Cercle extérieur, tronqué
        artists.extend(self._ax.plot(X4,Y3,'b')) # Cercle extérieur, tronqué
        artists.extend(self._ax.plot(X3,Y4,'b')) # Cercle extérieur, tronqué
        artists.extend(self._ax.plot(X4,Y4,'b')) # Cercle extérieur, tronqué
        artists.extend(self._ax.plot(X5,Y5,'b')) # Route ouest
        artists.extend(self._ax.plot(X6,Y5,'b')) # Route est
        artists.extend(self._ax.plot(X5,Y6,'b')) # Route ouest
        artists.extend(self._ax.plot(X6,Y6,'b')) # Route est
        artists.extend(self._ax.plot([-r/5, -r/5], [y_min, min(Y4)], 'b')) # Route sud
        artists.extend(self._ax.plot([-r/5, -r/5], [max(Y3), y_max], 'b')) # Route nord
        artists.extend(self._ax.plot([r/5, r/5], [y_min, min(Y4)], 'b')) # Route sud
        artists.extend(self._ax.plot([r/5, r/5], [max(Y3), y_max], 'b')) # Route nord

        return artists
