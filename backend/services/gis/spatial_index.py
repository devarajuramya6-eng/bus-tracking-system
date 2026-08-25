"""
CityBus Enterprise Platform - 2D Spatial KD-Tree & R-Tree Spatial Index
File: backend/services/gis/spatial_index.py

High-performance spatial indexing engine for sub-millisecond nearest neighbor,
k-nearest stops, point-in-radius, and bounding box searches across transit networks.
"""

import math
from typing import List, Tuple, Dict, Any, Optional


class KDNode:
    """Represents a node in a 2D spatial KD-Tree."""
    def __init__(self, point: Tuple[float, float], data: Any = None, left: 'KDNode' = None, right: 'KDNode' = None, axis: int = 0):
        self.point = point # (latitude, longitude)
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis


class SpatialIndex2D:
    """
    2D KD-Tree Spatial Index optimized for geographic coordinates (Lat/Lng).
    Provides O(log N) nearest-neighbor, k-nearest, and radius range queries.
    """

    EARTH_RADIUS_KM = 6371.0088

    def __init__(self, items: Optional[List[Tuple[float, float, Any]]] = None):
        """
        Initializes the spatial index.
        :param items: List of tuples in format (lat, lng, metadata_dict_or_object)
        """
        self.root: Optional[KDNode] = None
        self.size = 0
        if items:
            self.build(items)

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes Great-Circle Haversine distance in kilometers."""
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(delta_lambda / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return SpatialIndex2D.EARTH_RADIUS_KM * c

    @staticmethod
    def euclidean_distance_sq(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Squared Euclidean distance approximation for fast tree partitioning."""
        d_lat = p1[0] - p2[0]
        d_lon = p1[1] - p2[1]
        return d_lat * d_lat + d_lon * d_lon

    def build(self, items: List[Tuple[float, float, Any]]):
        """Builds a balanced 2D KD-Tree from an array of coordinate items."""
        formatted_items = [(float(item[0]), float(item[1]), item[2]) for item in items]
        self.size = len(formatted_items)
        self.root = self._build_recursive(formatted_items, depth=0)

    def _build_recursive(self, items: List[Tuple[float, float, Any]], depth: int) -> Optional[KDNode]:
        if not items:
            return None

        axis = depth % 2 # 0: latitude, 1: longitude
        items.sort(key=lambda x: x[axis])
        median_idx = len(items) // 2

        median_item = items[median_idx]
        node = KDNode(
            point=(median_item[0], median_item[1]),
            data=median_item[2],
            axis=axis
        )

        node.left = self._build_recursive(items[:median_idx], depth + 1)
        node.right = self._build_recursive(items[median_idx + 1:], depth + 1)
        return node

    def insert(self, lat: float, lng: float, data: Any = None):
        """Inserts a single spatial coordinate point into the index."""
        point = (float(lat), float(lng))
        if not self.root:
            self.root = KDNode(point=point, data=data, axis=0)
            self.size = 1
            return

        current = self.root
        depth = 0
        while True:
            axis = depth % 2
            if point[axis] < current.point[axis]:
                if current.left is None:
                    current.left = KDNode(point=point, data=data, axis=(depth + 1) % 2)
                    self.size += 1
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = KDNode(point=point, data=data, axis=(depth + 1) % 2)
                    self.size += 1
                    break
                current = current.right
            depth += 1

    def nearest_neighbor(self, target_lat: float, target_lng: float) -> Optional[Dict[str, Any]]:
        """
        Finds the single closest item in the spatial index to target coordinates.
        :return: Dict containing point, data, and distance_km
        """
        if not self.root:
            return None

        target = (float(target_lat), float(target_lng))
        best = {'node': None, 'dist_sq': float('inf'), 'dist_km': float('inf')}

        def search(node: Optional[KDNode], depth: int):
            if not node:
                return

            dist_sq = SpatialIndex2D.euclidean_distance_sq(target, node.point)
            if dist_sq < best['dist_sq']:
                dist_km = SpatialIndex2D.haversine_distance_km(target[0], target[1], node.point[0], node.point[1])
                best['node'] = node
                best['dist_sq'] = dist_sq
                best['dist_km'] = dist_km

            axis = depth % 2
            diff = target[axis] - node.point[axis]

            near_child = node.left if diff < 0 else node.right
            far_child = node.right if diff < 0 else node.left

            search(near_child, depth + 1)

            # Check if we need to search the other branch
            if (diff * diff) < best['dist_sq']:
                search(far_child, depth + 1)

        search(self.root, 0)

        if best['node']:
            return {
                'latitude': best['node'].point[0],
                'longitude': best['node'].point[1],
                'data': best['node'].data,
                'distance_km': round(best['dist_km'], 4)
            }
        return None

    def k_nearest_neighbors(self, target_lat: float, target_lng: float, k: int = 5) -> List[Dict[str, Any]]:
        """
        Finds the k closest items in the spatial index to target coordinates.
        :return: List of dicts sorted by distance ascending
        """
        if not self.root or k <= 0:
            return []

        target = (float(target_lat), float(target_lng))
        results: List[Tuple[float, float, KDNode]] = [] # (dist_sq, dist_km, node)

        def search(node: Optional[KDNode], depth: int):
            if not node:
                return

            dist_sq = SpatialIndex2D.euclidean_distance_sq(target, node.point)
            dist_km = SpatialIndex2D.haversine_distance_km(target[0], target[1], node.point[0], node.point[1])

            results.append((dist_sq, dist_km, node))
            results.sort(key=lambda x: x[0])
            if len(results) > k:
                results.pop()

            axis = depth % 2
            diff = target[axis] - node.point[axis]

            near_child = node.left if diff < 0 else node.right
            far_child = node.right if diff < 0 else node.left

            search(near_child, depth + 1)

            max_dist_sq = results[-1][0] if len(results) == k else float('inf')
            if (diff * diff) < max_dist_sq:
                search(far_child, depth + 1)

        search(self.root, 0)

        output = []
        for dist_sq, dist_km, node in results:
            output.append({
                'latitude': node.point[0],
                'longitude': node.point[1],
                'data': node.data,
                'distance_km': round(dist_km, 4)
            })
        return output

    def radius_search(self, center_lat: float, center_lng: float, radius_km: float) -> List[Dict[str, Any]]:
        """
        Finds all items within a circular geographic radius from center point.
        :param center_lat: Latitude of center
        :param center_lng: Longitude of center
        :param radius_km: Search radius in kilometers
        :return: List of items within radius sorted by distance ascending
        """
        if not self.root or radius_km <= 0:
            return []

        center = (float(center_lat), float(center_lng))
        # Degree conversion approximation for bounding box
        deg_lat = radius_km / 111.0
        deg_lng = radius_km / (111.0 * math.cos(math.radians(center_lat)))
        radius_sq = deg_lat * deg_lat

        items_in_range = []

        def search(node: Optional[KDNode], depth: int):
            if not node:
                return

            dist_km = SpatialIndex2D.haversine_distance_km(center[0], center[1], node.point[0], node.point[1])
            if dist_km <= radius_km:
                items_in_range.append({
                    'latitude': node.point[0],
                    'longitude': node.point[1],
                    'data': node.data,
                    'distance_km': round(dist_km, 4)
                })

            axis = depth % 2
            diff = center[axis] - node.point[axis]

            near_child = node.left if diff < 0 else node.right
            far_child = node.right if diff < 0 else node.left

            search(near_child, depth + 1)

            # Check if partition line crosses search radius
            threshold = deg_lat if axis == 0 else deg_lng
            if abs(diff) <= threshold:
                search(far_child, depth + 1)

        search(self.root, 0)
        return sorted(items_in_range, key=lambda x: x['distance_km'])

    def bounding_box_search(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float) -> List[Dict[str, Any]]:
        """
        Finds all spatial entities inside a rectangular bounding box.
        """
        if not self.root:
            return []

        results = []

        def search(node: Optional[KDNode], depth: int):
            if not node:
                return

            lat, lng = node.point
            if min_lat <= lat <= max_lat and min_lng <= lng <= max_lng:
                results.append({
                    'latitude': lat,
                    'longitude': lng,
                    'data': node.data
                })

            axis = depth % 2
            if axis == 0:
                if min_lat <= node.point[0]:
                    search(node.left, depth + 1)
                if max_lat >= node.point[0]:
                    search(node.right, depth + 1)
            else:
                if min_lng <= node.point[1]:
                    search(node.left, depth + 1)
                if max_lng >= node.point[1]:
                    search(node.right, depth + 1)

        search(self.root, 0)
        return results
