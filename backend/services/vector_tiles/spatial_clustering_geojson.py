"""
CityBus Enterprise Platform - High-Performance GeoJSON Spatial Point Clustering
File: backend/services/vector_tiles/spatial_clustering_geojson.py

Performs server-side spatial point clustering for massive transit networks:
- Clusters dense stop points and live buses into aggregated circle markers at low zoom levels (Zoom 10-13)
- Expands into individual pinpoint markers at street zoom levels (Zoom 14+)
"""

from typing import List, Dict, Any


class SpatialClusteringGeoJSON:
    @staticmethod
    def cluster_points(points: List[Dict[str, Any]], grid_size_deg: float = 0.01) -> Dict[str, Any]:
        """
        Clusters points using geographic grid binning.
        """
        bins: Dict[str, List[Dict[str, Any]]] = {}

        for p in points:
            lat = p.get('lat', 0.0)
            lng = p.get('lng', 0.0)
            bin_key = f"{int(lat / grid_size_deg)}_{int(lng / grid_size_deg)}"

            if bin_key not in bins:
                bins[bin_key] = []
            bins[bin_key].append(p)

        features = []
        for bin_key, b_points in bins.items():
            if len(b_points) == 1:
                pt = b_points[0]
                features.append({
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': [pt['lng'], pt['lat']]},
                    'properties': {'cluster': False, **pt}
                })
            else:
                avg_lat = sum(p['lat'] for p in b_points) / len(b_points)
                avg_lng = sum(p['lng'] for p in b_points) / len(b_points)
                features.append({
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': [avg_lng, avg_lat]},
                    'properties': {
                        'cluster': True,
                        'point_count': len(b_points),
                        'point_count_abbreviated': str(len(b_points))
                    }
                })

        return {
            'type': 'FeatureCollection',
            'features': features
        }
