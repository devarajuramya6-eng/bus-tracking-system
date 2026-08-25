"""
CityBus Enterprise Platform - Vector Tiles & Spatial GeoJSON Tests
File: tests/test_vector_tiles.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.vector_tiles.crowding_mvt_generator import CrowdingMVTGenerator
from services.vector_tiles.spatial_clustering_geojson import SpatialClusteringGeoJSON


class TestVectorTilesAndClustering(unittest.TestCase):
    def test_mvt_lat_lng_to_tile_xy(self):
        tile = CrowdingMVTGenerator.lat_lng_to_tile_xy(lat=16.5062, lng=80.6480, zoom=12)
        self.assertEqual(tile['zoom'], 12)
        self.assertGreater(tile['x'], 0)
        self.assertGreater(tile['y'], 0)

    def test_vector_layer_generation(self):
        features = [{'bus_id': 1, 'route_number': '27A', 'occupancy_pct': 75, 'lat': 16.5062, 'lng': 80.6480}]
        layer = CrowdingMVTGenerator.generate_vector_layer(features)
        self.assertEqual(layer['layer_name'], 'citybus_crowding_layer')
        self.assertEqual(len(layer['features']), 1)

    def test_spatial_clustering_geojson(self):
        points = [
            {'id': 1, 'lat': 16.5062, 'lng': 80.6480},
            {'id': 2, 'lat': 16.5064, 'lng': 80.6482}, # Close by (should cluster)
            {'id': 3, 'lat': 16.8000, 'lng': 80.9000}  # Far away
        ]
        fc = SpatialClusteringGeoJSON.cluster_points(points, grid_size_deg=0.01)
        self.assertEqual(fc['type'], 'FeatureCollection')
        self.assertGreater(len(fc['features']), 0)


if __name__ == '__main__':
    unittest.main()
