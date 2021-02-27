"""
Project name : TIPE_Yoann
Module name : test_road_item.py

Classes list in this module:
- TestRoadItem
------------------------------------------------------------------------------------------------------------------------
Author : Eric Ollivier
Create date : 27/02/2021
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Initial version
"""
import logging
import matplotlib.pyplot as plt
from unittest import TestCase

from parameters import DISTANCE
from road_objects.road_item import RoadItem
from roadmaps.linear_road import LinearRoad

logging.basicConfig(level=logging.DEBUG)

class TestRoadItem(TestCase):
    def setUp(self) -> None:
        """
        Initialise les jeux de données pour les tests
        """
        fig, ax = plt.subplots()
        ax.margins(0, 0)
        self.path = LinearRoad(ax).roadmap[0]
        self.road_items = [RoadItem(path=self.path) for i in range(2)]

    def test_distance(self):
        """
        Test le calcul de la distance
        """
        ECART_START = 10

        # Distance entre 2 positions successive
        dist_position = DISTANCE(self.path[0], self.path[1])
        logging.debug(f'TestRoadItem.test_distance : Distance entre 2 positions : {dist_position}')

        # Positionnement des RoadItem
        position2 = self.road_items[1].path[ECART_START]
        self.assertEqual(position2, self.path[ECART_START],
                         "Erreur dans la position du second item.")

        # Calcul de la distance entre les deux RoadItem
        self.assertEqual(dist_position*(ECART_START-1),
                         self.road_items[0].distance(position2),
                         "Erreur dans le calcul de la distance")
