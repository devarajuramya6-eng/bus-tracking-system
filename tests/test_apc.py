"""
CityBus Enterprise Platform - Automated Passenger Counting (APC) Unit Tests
File: tests/test_apc.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.apc.infrared_door_sensor import InfraredDoorSensor
from services.apc.weight_sensor_estimator import AirSuspensionWeightEstimator
from services.apc.camera_head_detector import OverheadCameraAPC


class TestAPCSystems(unittest.TestCase):
    def test_infrared_door_sensor_boarding(self):
        event = InfraredDoorSensor.process_beam_events("DOOR_FRONT", beam_a_timestamp=100.0, beam_b_timestamp=100.4)
        self.assertEqual(event['event_type'], 'PASSENGER_BOARDING_IN')
        self.assertEqual(event['count_change'], 1)

    def test_infrared_door_sensor_alighting(self):
        event = InfraredDoorSensor.process_beam_events("DOOR_REAR", beam_a_timestamp=100.5, beam_b_timestamp=100.1)
        self.assertEqual(event['event_type'], 'PASSENGER_ALIGHTING_OUT')
        self.assertEqual(event['count_change'], -1)

    def test_air_suspension_weight_estimation(self):
        est = AirSuspensionWeightEstimator.estimate_occupancy_from_pressure(
            front_air_bellow_bar=2.1,
            rear_air_bellow_bar=2.4
        )
        self.assertGreater(est['total_gross_weight_kg'], 11800.0)
        self.assertGreater(est['estimated_occupancy'], 0)

    def test_overhead_camera_head_counter(self):
        detections = [
            {'height_cm': 175, 'trajectory_vector_y': 0.8},
            {'height_cm': 160, 'trajectory_vector_y': 0.6},
            {'height_cm': 40, 'trajectory_vector_y': 0.8} # Filtered small luggage
        ]
        res = OverheadCameraAPC.process_vision_frame(detections)
        self.assertEqual(res['boardings_increment'], 2)


if __name__ == '__main__':
    unittest.main()
