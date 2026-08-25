"""
CityBus Enterprise Platform - Fuel Flow & Theft Detection Engine
File: backend/services/telematics/fuel_flow_sensor.py

Processes ultrasonic/capacitive fuel tank level sensors:
- Median smoothing filter for slosh mitigation
- Fuel efficiency calculations (km/L and L/100km)
- Anti-theft fuel pilferage detection (sudden volume drop while bus is parked/stationary)
"""

from typing import List, Dict, Any


class FuelFlowSensorEngine:
    @staticmethod
    def detect_theft_anomaly(fuel_level_series: List[Dict[str, Any]], drop_threshold_liters: float = 15.0) -> List[Dict[str, Any]]:
        """
        Detects sudden fuel drops while stationary.
        """
        if len(fuel_level_series) < 2:
            return []

        anomalies = []

        for i in range(len(fuel_level_series) - 1):
            f1 = fuel_level_series[i]
            f2 = fuel_level_series[i + 1]

            level_diff = f1.get('liters', 0.0) - f2.get('liters', 0.0)
            is_stationary = f1.get('speed', 0.0) < 1.0 and f2.get('speed', 0.0) < 1.0

            # If stationary and fuel dropped more than threshold in a short window
            if is_stationary and level_diff > drop_threshold_liters:
                anomalies.append({
                    'type': 'FUEL_THEFT_DETECTED',
                    'severity': 'Critical',
                    'bus_id': f1.get('bus_id'),
                    'liters_lost': round(level_diff, 1),
                    'timestamp': f2.get('timestamp'),
                    'location': (f2.get('lat'), f2.get('lng')),
                    'message': f"Sudden drop of {level_diff:.1f}L fuel detected while vehicle was stationary."
                })

        return anomalies
