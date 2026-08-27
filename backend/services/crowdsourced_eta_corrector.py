"""
CityBus Enterprise Platform - Crowdsourced Telemetry & Passenger ETA Correction Engine
File: backend/services/crowdsourced_eta_corrector.py

Fuses anonymized passenger mobile GPS pings while on board with vehicle OBD-II telemetry
to eliminate multipath satellite loss and adjust stop ETA countdowns in real time.
"""

from typing import Dict, List, Any, Optional


class CrowdsourcedETACorrector:
    """Combines rider location reports to refine vehicle arrival estimates."""

    @staticmethod
    def blend_telemetry_sources(vehicle_lat: float, vehicle_lng: float,
                                crowdsourced_pings: List[Dict[str, float]]) -> Dict[str, Any]:
        """Calculates weighted consensus coordinate from vehicle tracker and passenger phones."""
        if not crowdsourced_pings:
            return {"latitude": vehicle_lat, "longitude": vehicle_lng, "confidence": 0.85, "sample_size": 1}

        # Weight: Vehicle IoT = 0.70, Passenger cluster average = 0.30
        avg_pax_lat = sum(p["lat"] for p in crowdsourced_pings) / len(crowdsourced_pings)
        avg_pax_lng = sum(p["lng"] for p in crowdsourced_pings) / len(crowdsourced_pings)

        blended_lat = round(vehicle_lat * 0.70 + avg_pax_lat * 0.30, 6)
        blended_lng = round(vehicle_lng * 0.70 + avg_pax_lng * 0.30, 6)

        return {
            "latitude": blended_lat,
            "longitude": blended_lng,
            "confidence": min(0.99, 0.85 + len(crowdsourced_pings) * 0.03),
            "sample_size": len(crowdsourced_pings) + 1
        }
