"""
CityBus Enterprise Platform - Air Suspension Weight-Based Passenger Estimator
File: backend/services/apc/weight_sensor_estimator.py

Estimates passenger load from pneumatic air suspension bellows pressure transducers:
- Measures pressure (bar / PSI) across Front and Rear axle leveling valves
- Calculates gross vehicle payload (Gross Mass - Tare Mass) / 68kg standard passenger weight
- Validates and calibrates optical APC door counters
"""

from typing import Dict, Any


class AirSuspensionWeightEstimator:
    TARE_WEIGHT_KG = 11800.0 # Empty low-floor transit bus curb weight
    AVG_PASSENGER_MASS_KG = 68.0
    PRESSURE_TO_MASS_FACTOR_KG_PER_BAR = 1850.0

    @staticmethod
    def estimate_occupancy_from_pressure(front_air_bellow_bar: float, rear_air_bellow_bar: float) -> Dict[str, Any]:
        """
        Estimates onboard passengers from air bellows pressure sensors.
        """
        # Front axle has 2 bellows, Rear axle has 4 bellows
        front_mass_kg = front_air_bellow_bar * AirSuspensionWeightEstimator.PRESSURE_TO_MASS_FACTOR_KG_PER_BAR * 2.0
        rear_mass_kg = rear_air_bellow_bar * AirSuspensionWeightEstimator.PRESSURE_TO_MASS_FACTOR_KG_PER_BAR * 4.0

        total_gross_kg = front_mass_kg + rear_mass_kg
        payload_mass_kg = max(0.0, total_gross_kg - AirSuspensionWeightEstimator.TARE_WEIGHT_KG)

        estimated_pax = int(round(payload_mass_kg / AirSuspensionWeightEstimator.AVG_PASSENGER_MASS_KG))
        clamped_pax = max(0, min(80, estimated_pax))

        return {
            'front_bellow_pressure_bar': round(front_air_bellow_bar, 2),
            'rear_bellow_pressure_bar': round(rear_air_bellow_bar, 2),
            'total_gross_weight_kg': round(total_gross_kg, 1),
            'passenger_payload_kg': round(payload_mass_kg, 1),
            'estimated_occupancy': clamped_pax,
            'axle_load_distribution_pct': {
                'front_steer_axle': round((front_mass_kg / total_gross_kg) * 100.0, 1),
                'rear_drive_axle': round((rear_mass_kg / total_gross_kg) * 100.0, 1)
            }
        }
