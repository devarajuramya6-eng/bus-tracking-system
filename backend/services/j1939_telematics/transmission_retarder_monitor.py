"""
CityBus Enterprise Platform - Hydraulic / Electromagnetic Transmission Retarder Monitor
File: backend/services/j1939_telematics/transmission_retarder_monitor.py

Monitors transmission auxiliary retarder braking system:
- Retarder percent torque demand (SPN 520) & actual retarder torque
- Retarder hydraulic oil temperature (°C) & overheating protection
- Prolongs primary service brake friction lining life by 300%
"""

from typing import Dict, Any


class RetarderTelemetryMonitor:
    MAX_ALLOWABLE_RETARDER_TEMP_C = 145.0

    @staticmethod
    def process_retarder_telemetry(retarder_torque_pct: float, oil_temp_c: float) -> Dict[str, Any]:
        """
        Monitors auxiliary retarder braking health and thermal load.
        """
        is_overheating = oil_temp_c >= RetarderTelemetryMonitor.MAX_ALLOWABLE_RETARDER_TEMP_C
        is_active = retarder_torque_pct > 5.0

        return {
            'retarder_torque_percentage': round(retarder_torque_pct, 1),
            'retarder_oil_temp_celsius': round(oil_temp_c, 1),
            'is_retarder_engaged': is_active,
            'is_thermal_overload': is_overheating,
            'service_brakes_wear_mitigation_active': is_active,
            'status': 'CRITICAL_RETARDER_OVERHEAT' if is_overheating else ('RETARDER_BRAKING_ACTIVE' if is_active else 'RETARDER_STANDBY')
        }
