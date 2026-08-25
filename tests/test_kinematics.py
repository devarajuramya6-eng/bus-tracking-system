"""
CityBus Enterprise Platform - Kinematics & Sensor Fusion Unit Tests
File: tests/test_kinematics.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.kinematics.imu_sensor_fusion import IMUSensorFusion
from services.kinematics.grade_resistance_model import VehiclePhysicsModel
from services.kinematics.dead_reckoning_engine import DeadReckoningEngine


class TestKinematicsAndPhysics(unittest.TestCase):
    def test_imu_kalman_sensor_fusion(self):
        fusion = IMUSensorFusion()
        fused = fusion.process_telemetry_frame(
            gps_lat=16.5062,
            gps_lng=80.6480,
            speed_kmh=35.0,
            heading_deg=90.0,
            ax=0.8,
            ay=0.2,
            dt=0.1
        )
        self.assertIn('fused_latitude', fused)
        self.assertIn('fused_longitude', fused)
        self.assertAlmostEqual(fused['fused_latitude'], 16.5062, places=2)

    def test_vehicle_tractive_effort_physics(self):
        effort = VehiclePhysicsModel.calculate_tractive_effort(
            speed_kmh=40.0,
            accel_mps2=0.5,
            passenger_count=35,
            road_grade_pct=2.0
        )
        self.assertIn('total_tractive_force_n', effort)
        self.assertGreater(effort['required_power_kw'], 0.0)
        self.assertGreater(effort['f_grade_newtons'], 0.0)

    def test_dead_reckoning_odometry(self):
        dr = DeadReckoningEngine.propagate_position(
            start_lat=16.5062,
            start_lng=80.6480,
            start_heading_deg=90.0, # Heading East
            wheel_pulses_delta=480, # 10 wheel revolutions ~ 33 meters
            yaw_rate_deg_per_sec=0.0,
            dt_seconds=2.0
        )
        self.assertGreater(dr['distance_traveled_m'], 30.0)
        self.assertGreater(dr['estimated_lng'], 80.6480) # Traveled East
        self.assertEqual(dr['navigation_mode'], 'DEAD_RECKONING_ACTIVE')


if __name__ == '__main__':
    unittest.main()
