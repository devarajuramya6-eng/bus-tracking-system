"""
CityBus Enterprise Platform - 6-Wheel TPMS Telemetry Parser & Leak Detector
File: backend/services/tire_health/tpms_telemetry_parser.py

Monitors direct valve-mounted TPMS sensors across commercial heavy bus wheels:
- Positions: Front Left (FL), Front Right (FR), Rear Left Outer (RLO), Rear Left Inner (RLI), Rear Right Outer (RRO), Rear Right Inner (RRI)
- Cold inflation baseline: 8.5 bar (123 PSI)
- Low Pressure Warning (< 7.2 bar) & Thermal Overheat Warning (> 80°C)
"""

from typing import Dict, Any, List


class TPMSTelemetryParser:
    NOMINAL_PRESSURE_BAR = 8.5
    LOW_PRESSURE_THRESHOLD_BAR = 7.2
    HIGH_TEMP_THRESHOLD_C = 80.0

    @staticmethod
    def evaluate_wheel_tpms(wheel_position: str, pressure_bar: float, temperature_c: float, pressure_drop_rate_bar_hr: float = 0.0) -> Dict[str, Any]:
        """
        Evaluates single wheel TPMS status.
        """
        is_low_pressure = pressure_bar < TPMSTelemetryParser.LOW_PRESSURE_THRESHOLD_BAR
        is_high_temp = temperature_c > TPMSTelemetryParser.HIGH_TEMP_THRESHOLD_C
        is_slow_puncture = pressure_drop_rate_bar_hr > 0.3 # Losing > 0.3 bar/hr

        severity = 'CRITICAL_PUNCTURE' if (pressure_bar < 6.0 or is_slow_puncture) else ('WARNING' if (is_low_pressure or is_high_temp) else 'NOMINAL')

        return {
            'wheel_position': wheel_position,
            'pressure_bar': round(pressure_bar, 2),
            'pressure_psi': round(pressure_bar * 14.5038, 1),
            'temperature_celsius': round(temperature_c, 1),
            'leak_rate_bar_per_hr': round(pressure_drop_rate_bar_hr, 2),
            'is_underinflated': is_low_pressure,
            'is_overheating': is_high_temp,
            'is_puncture_detected': is_slow_puncture,
            'status': severity
        }
