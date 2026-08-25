"""
CityBus Enterprise Platform - Spatial GIS & Network Algorithms Unit Tests
File: tests/test_gis.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.gis.spatial_index import SpatialIndex2D
from services.gis.polyline_encoder import PolylineEncoder
from services.gis.geofence_engine import GeofenceEngine, GeofenceZone
from services.gis.map_matching import MapMatchingEngine


class TestSpatialGIS(unittest.TestCase):
    def test_kd_tree_spatial_index(self):
        stops = [
            (16.5100, 80.6175, "PNBS"),
            (16.5020, 80.6475, "Benz Circle"),
            (16.5180, 80.6200, "Railway Station"),
            (16.4950, 80.6780, "Autonagar")
        ]
        index = SpatialIndex2D(stops)
        self.assertEqual(index.size, 4)

        # Nearest neighbor to PNBS
        nearest = index.nearest_neighbor(16.5105, 80.6170)
        self.assertIsNotNone(nearest)
        self.assertEqual(nearest['data'], "PNBS")

        # Radius search 2km around Benz Circle
        results = index.radius_search(16.5020, 80.6475, 2.0)
        self.assertTrue(any(r['data'] == 'Benz Circle' for r in results))

    def test_polyline_encoder_and_decoder(self):
        coords = [
            (16.5100, 80.6175),
            (16.5060, 80.6300),
            (16.5020, 80.6475)
        ]
        encoded = PolylineEncoder.encode(coords)
        self.assertIsInstance(encoded, str)
        self.assertGreater(len(encoded), 5)

        decoded = PolylineEncoder.decode(encoded)
        self.assertEqual(len(decoded), len(coords))
        self.assertAlmostEqual(decoded[0][0], coords[0][0], places=4)
        self.assertAlmostEqual(decoded[0][1], coords[0][1], places=4)

    def test_geofence_containment(self):
        engine = GeofenceEngine()
        zone = GeofenceZone(
            zone_id="ZONE_PNBS",
            name="PNBS Terminal",
            zone_type="CIRCLE",
            category="DEPOT",
            center=(16.5100, 80.6175),
            radius_meters=300.0,
            max_speed_kmh=15.0
        )
        engine.add_zone(zone)

        # Inside zone with overspeed
        alerts = engine.evaluate_location(16.5102, 80.6174, current_speed_kmh=25.0)
        self.assertEqual(len(alerts), 1)
        self.assertTrue(alerts[0]['is_speed_violation'])
        self.assertEqual(alerts[0]['zone_id'], "ZONE_PNBS")

    def test_map_matching_road_snap(self):
        route_line = [
            (16.5100, 80.6175),
            (16.5100, 80.6300),
            (16.5100, 80.6400)
        ]
        # GPS ping with slight lateral noise
        res = MapMatchingEngine.match_to_polyline(16.5102, 80.6250, route_line, max_snap_distance_m=50.0)
        self.assertTrue(res['is_on_route'])
        self.assertAlmostEqual(res['snapped_lat'], 16.5100, places=3)


if __name__ == '__main__':
    unittest.main()
