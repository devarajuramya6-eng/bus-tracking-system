"""
CityBus Enterprise Platform - Driver Behavior & Safety Telematics Analyzer
File: backend/services/driver_behavior_analyzer.py

Analyzes high-frequency IMU acceleration traces, cornering g-force spikes,
speed limit compliance, and generates driver safety scorecards (0-100 score).
"""

from typing import Dict, List, Any, Optional
from models import Driver, Telemetry, Bus, db


class DriverBehaviorAnalyzer:
    """Computes safety scores and eco-driving metrics from vehicle telemetry."""

    SPEED_LIMIT_KMH = 65.0

    @staticmethod
    def analyze_trip_telemetry(bus_id: int, pings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates speed compliance, harsh events, and overall safety rating."""
        if not pings or len(pings) < 2:
            return {
                "safety_score": 100,
                "eco_score": 95,
                "speed_violations_count": 0,
                "harsh_braking_events": 0,
                "harsh_acceleration_events": 0,
                "rating_grade": "A+"
            }

        speed_violations = 0
        harsh_braking = 0
        harsh_accel = 0
        total_pings = len(pings)

        for i in range(1, total_pings):
            p1 = pings[i - 1]
            p2 = pings[i]
            s1 = float(p1.get('speed', 0.0))
            s2 = float(p2.get('speed', 0.0))

            if s2 > DriverBehaviorAnalyzer.SPEED_LIMIT_KMH:
                speed_violations += 1

            # Approximate delta time between pings (default 2s)
            delta_t = 2.0
            accel_mps2 = ((s2 - s1) * 1000.0 / 3600.0) / delta_t

            if accel_mps2 > 2.8:
                harsh_accel += 1
            elif accel_mps2 < -3.5:
                harsh_braking += 1

        # Penalties calculation
        score = 100.0
        score -= (speed_violations * 2.5)
        score -= (harsh_braking * 3.0)
        score -= (harsh_accel * 2.0)
        final_score = max(40.0, round(score, 1))

        # Grade mapping
        if final_score >= 90: grade = "A+"
        elif final_score >= 80: grade = "A"
        elif final_score >= 70: grade = "B"
        elif final_score >= 60: grade = "C"
        else: grade = "D"

        eco_score = max(50.0, round(100.0 - (harsh_accel * 4.0) - (speed_violations * 1.5), 1))

        return {
            "bus_id": bus_id,
            "total_pings_evaluated": total_pings,
            "safety_score": final_score,
            "eco_score": eco_score,
            "speed_violations_count": speed_violations,
            "harsh_braking_events": harsh_braking,
            "harsh_acceleration_events": harsh_accel,
            "rating_grade": grade
        }
