"""
CityBus Enterprise Platform - Chassis Rosette Strain Gauge Stress Monitor
File: backend/services/chassis_structural/strain_gauge_fatigue_telemetry.py

Monitors micro-strain (ue) sensors on high-stress bus chassis points:
- Sensor Locations: FRONT_AXLE_CROSSMEMBER, MID_CHASSIS_LONGITUDINAL, REAR_SUSPENSION_HANGER
- Converts microstrain to mechanical stress: $\sigma = E \cdot \epsilon$ (Structural Steel $E = 210\text{ GPa}$)
- Yield Stress Warning: Yield strength $\sigma_y = 355\text{ MPa}$ (Flags plastic deformation risk)
"""

from typing import Dict, Any


class ChassisStrainGaugeAuditor:
    STEEL_YOUNGS_MODULUS_MPA = 210000.0 # 210 GPa
    YIELD_STRENGTH_MPA = 355.0

    @staticmethod
    def calculate_mechanical_stress(sensor_location: str,
                                   measured_microstrain_ue: float) -> Dict[str, Any]:
        """
        Converts microstrain to stress in Megapascals (MPa).
        """
        # 1 microstrain = 1e-6 strain
        strain = measured_microstrain_ue * 1e-6
        stress_mpa = strain * ChassisStrainGaugeAuditor.STEEL_YOUNGS_MODULUS_MPA
        stress_ratio_pct = (stress_mpa / ChassisStrainGaugeAuditor.YIELD_STRENGTH_MPA) * 100.0

        is_yield_exceeded = stress_mpa >= ChassisStrainGaugeAuditor.YIELD_STRENGTH_MPA

        return {
            'sensor_location': sensor_location,
            'microstrain_ue': round(measured_microstrain_ue, 1),
            'calculated_stress_mpa': round(stress_mpa, 2),
            'yield_strength_mpa': ChassisStrainGaugeAuditor.YIELD_STRENGTH_MPA,
            'stress_to_yield_ratio_pct': round(stress_ratio_pct, 1),
            'is_plastic_deformation_risk': is_yield_exceeded,
            'structural_health_status': 'DANGER_PLASTIC_DEFORMATION' if is_yield_exceeded else 'ELASTIC_RANGE_HEALTHY'
        }
