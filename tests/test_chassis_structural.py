"""
CityBus Enterprise Platform - Chassis Structural Integrity Tests
File: tests/test_chassis_structural.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.chassis_structural.strain_gauge_fatigue_telemetry import ChassisStrainGaugeAuditor
from services.chassis_structural.rainflow_cycle_counting import RainflowCycleCounter
from services.chassis_structural.chassis_crack_risk_predictor import ChassisCrackPredictor


class TestChassisStructural(unittest.TestCase):
    def test_strain_gauge_stress_calculation(self):
        stress = ChassisStrainGaugeAuditor.calculate_mechanical_stress(
            sensor_location="FRONT_AXLE_CROSSMEMBER",
            measured_microstrain_ue=500.0 # 500 ue * 210 GPa = 105 MPa
        )
        self.assertEqual(stress['calculated_stress_mpa'], 105.0)
        self.assertFalse(stress['is_plastic_deformation_risk'])
        self.assertEqual(stress['structural_health_status'], 'ELASTIC_RANGE_HEALTHY')

    def test_rainflow_fatigue_damage_counting(self):
        peaks_valleys = [50.0, 150.0, 80.0, 200.0, 60.0]
        damage = RainflowCycleCounter.compute_fatigue_damage(peaks_valleys)
        self.assertGreater(damage['max_stress_range_mpa'], 100.0)
        self.assertGreater(damage['structural_integrity_life_pct'], 90.0)

    def test_chassis_crack_risk_prediction(self):
        crack = ChassisCrackPredictor.predict_crack_risk(
            accumulated_odometer_km=450000.0,
            rough_road_severity_factor=1.0
        )
        self.assertGreater(crack['weld_crack_initiation_prob_pct'], 5.0)
        self.assertIn('odometer_km', crack)


if __name__ == '__main__':
    unittest.main()
