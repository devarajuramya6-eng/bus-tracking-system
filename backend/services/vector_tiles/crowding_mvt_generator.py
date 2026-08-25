"""
CityBus Enterprise Platform - Mapbox Vector Tile (MVT) Crowding Layer Generator
File: backend/services/vector_tiles/crowding_mvt_generator.py

Generates vector map tile features for transit crowding visualization:
- Projects lat/lng to Web Mercator (EPSG:3857) tile coordinate space [0..4096]
- Encodes route segment occupancy density (Low, Medium, Heavy, Crush)
"""

import math
from typing import List, Dict, Any


class CrowdingMVTGenerator:
    TILE_EXTENT = 4096

    @staticmethod
    def lat_lng_to_tile_xy(lat: float, lng: float, zoom: int) -> Dict[str, int]:
        """
        Converts lat/lng to global tile coordinate numbers.
        """
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x_tile = int((lng + 180.0) / 360.0 * n)
        y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return {'zoom': zoom, 'x': x_tile, 'y': y_tile}

    @staticmethod
    def generate_vector_layer(features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds vector tile layer JSON representation.
        """
        encoded_features = []
        for f in features:
            encoded_features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [f.get('lng', 80.6480), f.get('lat', 16.5062)]
                },
                'properties': {
                    'bus_id': f.get('bus_id'),
                    'route_number': f.get('route_number'),
                    'occupancy_pct': f.get('occupancy_pct', 50),
                    'crowd_color': '#10B981' if f.get('occupancy_pct', 50) < 60 else ('#F59E0B' if f.get('occupancy_pct', 50) < 85 else '#EF4444')
                }
            })

        return {
            'layer_name': 'citybus_crowding_layer',
            'version': 2,
            'extent': CrowdingMVTGenerator.TILE_EXTENT,
            'features': encoded_features
        }
