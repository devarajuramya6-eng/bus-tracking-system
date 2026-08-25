"""
CityBus Enterprise Platform - CSA, RAPTOR & Isochrone Routing Unit Tests
File: tests/test_advanced_routing.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.routing.csa_router import CSARouter, TimetableConnection
from services.routing.raptor_router import RAPTORRouter, RAPTORRoute
from services.routing.isochrone_generator import IsochroneGenerator


class TestAdvancedRoutingAlgorithms(unittest.TestCase):
    def test_csa_earliest_arrival(self):
        connections = [
            TimetableConnection(dep_stop=1, arr_stop=2, dep_time=360, arr_time=380, trip_id="T1", route_num="27A"),
            TimetableConnection(dep_stop=2, arr_stop=3, dep_time=385, arr_time=410, trip_id="T2", route_num="5K")
        ]
        csa = CSARouter(connections)
        journey = csa.find_earliest_arrival(origin_stop=1, dest_stop=3, departure_time_min=350)
        self.assertIsNotNone(journey)
        self.assertEqual(journey['arrival_min'], 410)
        self.assertEqual(journey['total_duration_minutes'], 60)
        self.assertEqual(journey['transfers'], 1)

    def test_raptor_pareto_routing(self):
        routes = [
            RAPTORRoute(route_id=1, route_number="27A", stops=[101, 102, 103, 104]),
            RAPTORRoute(route_id=2, route_number="5K", stops=[103, 105, 106])
        ]
        raptor = RAPTORRouter(routes)
        solutions = raptor.route_query(origin_stop=101, dest_stop=106, max_rounds=2)
        self.assertGreater(len(solutions), 0)
        self.assertLessEqual(solutions[0]['transfers'], 1)

    def test_isochrone_generation(self):
        iso = IsochroneGenerator.generate_isochrones(center_lat=16.5100, center_lng=80.6175, time_intervals_min=[15, 30])
        self.assertEqual(len(iso['isochrones']), 2)
        self.assertGreater(iso['isochrones'][1]['radius_km'], iso['isochrones'][0]['radius_km'])


if __name__ == '__main__':
    unittest.main()
