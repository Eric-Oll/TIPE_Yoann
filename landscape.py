"""
Création du fond de carte
"""
import numpy as np

# b) Création du rond-point
def f1(x,r): # Création de la partie positive du cercle extérieur, tronqué
    y = x**2-63*r/64
    return np.sqrt(np.sqrt(y/abs(y))*(r**2*(np.sqrt((abs(abs(x)-r/8))/(abs(x)-r/8)))-(x**2)))

def f2(x,r): # Création de la partie négative du cercle extérieur, tronqué
    y = x**2-63*r/64
    return -np.sqrt(np.sqrt(y/abs(y))*(r**2*(np.sqrt((abs(abs(x)-r/8))/(abs(x)-r/8)))-(x**2)))

def create_landscape(ax, r1, r2, r):
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
