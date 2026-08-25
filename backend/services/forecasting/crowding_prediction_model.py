"""
CityBus Enterprise Platform - Onboard Bus Crowding Prediction Model
File: backend/services/forecasting/crowding_prediction_model.py

Predicts onboard passenger crowding levels for future trips:
- SEATS_AVAILABLE (Occupancy < 50%)
- FEW_SEATS_AVAILABLE (50% <= Occupancy < 85%)
- STANDING_ROOM_ONLY (85% <= Occupancy <= 100%)
- FULL_CRUSH_LOAD (Occupancy > 100% - Boarding restricted)
"""

from typing import Dict, Any


class CrowdingPredictionModel:
    @staticmethod
    def predict_trip_crowding(departure_hour: int, is_school_working_day: bool = True, route_type: str = "CORRIDOR") -> Dict[str, Any]:
        """
        Predicts crowding probability for a departure time.
        """
        is_morning_peak = 7 <= departure_hour <= 9
        is_evening_peak = 17 <= departure_hour <= 19

        expected_occupancy_pct = 40.0

        if is_morning_peak:
            expected_occupancy_pct = 92.0 if is_school_working_day else 75.0
        elif is_evening_peak:
            expected_occupancy_pct = 88.0
        elif 12 <= departure_hour <= 14:
            expected_occupancy_pct = 55.0

        if expected_occupancy_pct > 90.0:
            crowding_level = 'STANDING_ROOM_ONLY'
            color = '#EF4444'
        elif expected_occupancy_pct >= 60.0:
            crowding_level = 'FEW_SEATS_AVAILABLE'
            color = '#F59E0B'
        else:
            crowding_level = 'SEATS_AVAILABLE'
            color = '#10B981'

        return {
            'departure_hour': departure_hour,
            'expected_occupancy_pct': round(expected_occupancy_pct, 1),
            'crowding_level': crowding_level,
            'badge_color': color,
            'advice': 'Board at front door. Limited seating available.' if expected_occupancy_pct > 80 else 'Comfortable seating available.'
        }
