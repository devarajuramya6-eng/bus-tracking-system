"""
CityBus Enterprise Platform - Pedestrian Routing & Catchment Tests
File: tests/test_pedestrian_routing.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.pedestrian_routing.walk_shed_graph import PedestrianWalkshedGraph, SidewalkEdge
from services.pedestrian_routing.multimodal_catchment_polygon import CatchmentPolygonGenerator
from services.pedestrian_routing.elevation_gradient_penalty import ElevationWalkingPenalty


class TestPedestrianRouting(unittest.TestCase):
    def test_pedestrian_wheelchair_impedance(self):
        edge1 = SidewalkEdge(1, 2, length_m=100.0, has_curb_cut=False)
        graph = PedestrianWalkshedGraph([edge1])
        res = graph.calculate_path_impedance(is_wheelchair=True)
        self.assertEqual(res[0]['effective_impedance_m'], 1000.0) # 10x penalty

    def test_catchment_polygon_generation(self):
        poly = CatchmentPolygonGenerator.generate_walkshed_geometry(center_lat=16.5062, center_lng=80.6480, walk_minutes=[5, 10])
        self.assertEqual(len(poly['walksheds']), 2)
        self.assertEqual(poly['walksheds'][0]['walk_time_minutes'], 5)
        self.assertGreater(poly['walksheds'][0]['estimated_population_served'], 1000)

    def test_tobler_hiking_elevation_penalty(self):
        speed_flat = ElevationWalkingPenalty.calculate_slope_walking_speed(distance_m=200.0, elevation_gain_m=0.0)
        speed_steep = ElevationWalkingPenalty.calculate_slope_walking_speed(distance_m=200.0, elevation_gain_m=30.0) # 15% slope
        self.assertGreater(speed_flat['adjusted_walking_speed_kmh'], speed_steep['adjusted_walking_speed_kmh'])
        self.assertTrue(speed_steep['is_steep_incline'])


if __name__ == '__main__':
    unittest.main()
