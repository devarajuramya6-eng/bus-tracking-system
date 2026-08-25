"""
CityBus Enterprise Platform - In-Cabin CO2 Air Quality & Fresh Air Damper Control
File: backend/services/hvac_comfort/co2_air_quality_ventilator.py

Monitors interior passenger cabin air quality:
- CO2 < 800 ppm: Clean ambient (Fresh air damper 20% open)
- 800 - 1200 ppm: Moderate crowd (Fresh air damper 50% open)
- > 1200 ppm: Stale air drowsiness risk (Motorized roof damper 100% full purge)
"""

from typing import Dict, Any


class CabinAirQualityVentilator:
    @staticmethod
    def evaluate_cabin_air_quality(co2_ppm: float, tvoc_ppb: float = 180.0) -> Dict[str, Any]:
        """
        Calculates motorized fresh air damper position.
        """
        if co2_ppm >= 1200.0:
            damper_pct = 100
            quality = 'STALE_AIR_PURGE_TRIGGERED'
            status = 'WARNING'
        elif co2_ppm >= 850.0:
            damper_pct = 55
            quality = 'MODERATE_VENTILATION_ACTIVE'
            status = 'NOMINAL'
        else:
            damper_pct = 20
            quality = 'FRESH_AIR_OPTIMAL'
            status = 'NOMINAL'

        return {
            'measured_co2_ppm': round(co2_ppm, 1),
            'measured_tvoc_ppb': round(tvoc_ppb, 1),
            'fresh_air_damper_position_pct': damper_pct,
            'ventilation_mode': quality,
            'passenger_alertness_status': 'PROTECTED' if co2_ppm < 1200 else 'DROWSINESS_RISK',
            'system_status': status
        }
