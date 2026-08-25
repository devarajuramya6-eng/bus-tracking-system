"""
CityBus Enterprise Platform - Polyline Encoder & Douglas-Peucker Simplification
File: backend/services/gis/polyline_encoder.py

Encodes, decodes, simplifies, and analyzes route coordinate chains:
- Precision 5 and Precision 6 Google Encoded Polyline Algorithm
- Ramer-Douglas-Peucker (RDP) polyline simplification for bandwidth reduction
- Polyline segment length and cumulative distance interpolation
"""

import math
from typing import List, Tuple, Dict, Any


class PolylineEncoder:
    """Standard Google Polyline encoder and geometric simplifier."""

    @staticmethod
    def encode(points: List[Tuple[float, float]], precision: int = 5) -> str:
        """
        Encodes a list of (lat, lng) tuples into an encoded polyline ASCII string.
        :param points: List of (lat, lng) tuples
        :param precision: Decimal precision (default 5 for 1e5 standard)
        :return: Encoded polyline string
        """
        if not points:
            return ""

        factor = 10 ** precision
        output = []
        prev_lat = 0
        prev_lng = 0

        for point in points:
            lat = int(round(point[0] * factor))
            lng = int(round(point[1] * factor))

            d_lat = lat - prev_lat
            d_lng = lng - prev_lng

            prev_lat = lat
            prev_lng = lng

            output.append(PolylineEncoder._encode_value(d_lat))
            output.append(PolylineEncoder._encode_value(d_lng))

        return "".join(output)

    @staticmethod
    def _encode_value(value: int) -> str:
        value = ~(value << 1) if value < 0 else (value << 1)
        chunks = []
        while value >= 0x20:
            chunks.append(chr((0x20 | (value & 0x1f)) + 63))
            value >>= 5
        chunks.append(chr(value + 63))
        return "".join(chunks)

    @staticmethod
    def decode(polyline_str: str, precision: int = 5) -> List[Tuple[float, float]]:
        """
        Decodes an encoded polyline ASCII string back into a list of (lat, lng) tuples.
        """
        if not polyline_str:
            return []

        factor = 10 ** precision
        points = []
        index = 0
        lat = 0
        lng = 0
        length = len(polyline_str)

        while index < length:
            # Decode Latitude
            b = 0
            shift = 0
            result = 0
            while True:
                b = ord(polyline_str[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            d_lat = ~(result >> 1) if (result & 1) else (result >> 1)
            lat += d_lat

            # Decode Longitude
            shift = 0
            result = 0
            while True:
                b = ord(polyline_str[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            d_lng = ~(result >> 1) if (result & 1) else (result >> 1)
            lng += d_lng

            points.append((lat / factor, lng / factor))

        return points

    @staticmethod
    def perpendicular_distance(point: Tuple[float, float], line_start: Tuple[float, float], line_end: Tuple[float, float]) -> float:
        """Calculates perpendicular distance from point to line segment."""
        if line_start == line_end:
            d_lat = point[0] - line_start[0]
            d_lon = point[1] - line_start[1]
            return math.sqrt(d_lat * d_lat + d_lon * d_lon)

        x0, y0 = point
        x1, y1 = line_start
        x2, y2 = line_end

        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return numerator / denominator if denominator > 0 else 0.0

    @staticmethod
    def simplify(points: List[Tuple[float, float]], tolerance_degrees: float = 0.0001) -> List[Tuple[float, float]]:
        """
        Simplifies a polyline using the Ramer-Douglas-Peucker algorithm.
        :param points: List of (lat, lng) tuples
        :param tolerance_degrees: Tolerance in coordinate degrees (e.g. 0.0001 ~ 11 meters)
        :return: Simplified list of coordinate points
        """
        if len(points) <= 2:
            return points

        max_dist = 0.0
        index = 0
        end = len(points) - 1

        for i in range(1, end):
            dist = PolylineEncoder.perpendicular_distance(points[i], points[0], points[end])
            if dist > max_dist:
                max_dist = dist
                index = i

        if max_dist > tolerance_degrees:
            left_segment = PolylineEncoder.simplify(points[:index + 1], tolerance_degrees)
            right_segment = PolylineEncoder.simplify(points[index:], tolerance_degrees)
            return left_segment[:-1] + right_segment
        else:
            return [points[0], points[end]]

    @staticmethod
    def compute_cumulative_distances(points: List[Tuple[float, float]]) -> List[float]:
        """Returns array of cumulative distances along the polyline in kilometers."""
        if not points:
            return []

        distances = [0.0]
        accum = 0.0
        R = 6371.0088

        for i in range(len(points) - 1):
            lat1, lon1 = points[i]
            lat2, lon2 = points[i + 1]

            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)
            d_phi = math.radians(lat2 - lat1)
            d_lam = math.radians(lon2 - lon1)

            a = (math.sin(d_phi / 2.0) ** 2 +
                 math.cos(phi1) * math.cos(phi2) *
                 math.sin(d_lam / 2.0) ** 2)
            c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
            dist_km = R * c
            accum += dist_km
            distances.append(round(accum, 4))

        return distances
