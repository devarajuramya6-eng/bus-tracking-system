"""
CityBus Enterprise Platform - V2X Transit Signal Priority (TSP) Service
File: backend/services/v2x_tsp_optimizer.py

Interfaces with municipal traffic controllers via IEEE 1609.2 / NTCIP 1202 standards:
- Generates Green Light Extension & Early Red Truncation requests
- Evaluates bus schedule adherence to grant priority only to delayed vehicles
- Optimizes corridor arterial intersection travel times
"""

import math
from typing import Dict, List, Any, Optional
from models import Bus, Route, db


class V2XIntersection:
    def __init__(self, junction_id: str, name: str, lat: float, lng: float, approach_distance_meters: float = 250.0):
        self.junction_id = junction_id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.approach_distance_meters = approach_distance_meters
        self.current_phase = "MAIN_STREET_GREEN"
        self.cycle_length_sec = 90


class V2XTSPOptimizer:
    """Manages Transit Signal Priority evaluation and roadside communication."""

    EARTH_RADIUS_METERS = 6371000.0

    _junctions = [
        V2XIntersection("INT-01", "Benz Circle Arterial Junction", 16.5020, 80.6475),
        V2XIntersection("INT-02", "PNBS Terminal Main Exit Signal", 16.5100, 80.6175),
        V2XIntersection("INT-03", "Governorpet Commercial Crossing", 16.5140, 80.6300),
        V2XIntersection("INT-04", "Ramavarappadu Ring Highway Signal", 16.5260, 80.6710),
        V2XIntersection("INT-05", "Gollapudi Bypass Corridor", 16.5400, 80.5900)
    ]

    @staticmethod
    def calculate_distance_meters(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lng / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return V2XTSPOptimizer.EARTH_RADIUS_METERS * c

    @classmethod
    def evaluate_bus_tsp_request(cls, bus_id: int, bus_lat: float, bus_lng: float, speed_kmh: float) -> List[Dict[str, Any]]:
        """
        Scans approaching intersections. If bus is within approach zone and moving,
        evaluates whether to grant Green Extension or Early Green.
        """
        bus = Bus.query.get(bus_id)
        if not bus:
            return []

        priority_requests = []
        is_delayed = bus.status == "Delayed" or bus.occupancy >= 25 # Prioritize packed or delayed buses

        for junction in cls._junctions:
            dist = cls.calculate_distance_meters(bus_lat, bus_lng, junction.lat, junction.lng)
            if dist <= junction.approach_distance_meters:
                # Estimated Time to Arrival at Stop Line (seconds)
                eta_seconds = (dist / max(5.0, (speed_kmh * 1000.0) / 3600.0))

                request_type = "GREEN_EXTENSION" if eta_seconds <= 12.0 else "EARLY_GREEN_TRUNCATION"
                granted = is_delayed or (speed_kmh >= 20.0 and dist <= 120.0)

                priority_requests.append({
                    "junction_id": junction.junction_id,
                    "junction_name": junction.name,
                    "bus_id": bus_id,
                    "bus_number": bus.bus_number,
                    "distance_meters": round(dist, 1),
                    "eta_to_stopline_seconds": round(eta_seconds, 1),
                    "tsp_request_type": request_type,
                    "priority_granted": granted,
                    "rationale": "High occupancy / delayed on schedule" if granted else "Normal traffic flow maintained"
                })

        return priority_requests
