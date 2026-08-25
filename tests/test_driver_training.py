"""
CityBus Enterprise Platform - Driver Training & Telematics Scorecard Tests
File: tests/test_driver_training.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.driver_training.driver_safety_scorecard import DriverSafetyScorecardEngine
from services.driver_training.defensive_driving_recommender import DefensiveDrivingCoachingEngine
from services.driver_training.fuel_efficient_eco_driving import EcoDrivingAnalyzer


class TestDriverTraining(unittest.TestCase):
    def test_driver_safety_scorecard_master(self):
        scorecard = DriverSafetyScorecardEngine.compute_scorecard(
            driver_id=1,
            driver_name="Ravi",
            distance_km=300.0,
            harsh_brakes=1,
            rapid_accels=0,
            harsh_turns=0,
            overspeed_events=0
        )
        self.assertGreaterEqual(scorecard['safety_score'], 90.0)
        self.assertEqual(scorecard['performance_tier'], 'MASTER_CAPTAIN')
        self.assertEqual(scorecard['driver_safety_incentive_inr'], 500.0)

    def test_defensive_driving_coaching_recommendations(self):
        modules = DefensiveDrivingCoachingEngine.recommend_training(harsh_brakes=3, harsh_turns=0, overspeed_count=1)
        self.assertEqual(len(modules), 2)
        self.assertEqual(modules[0]['module_id'], 'MOD_SAFE_STOP')

    def test_eco_driving_coasting_analyzer(self):
        eco = EcoDrivingAnalyzer.evaluate_trip_eco_efficiency(
            total_distance_km=100.0,
            coasting_distance_km=22.0, # 22%
            wot_events_count=1
        )
        self.assertGreater(eco['eco_driving_score'], 80.0)
        self.assertEqual(eco['grade'], 'GOLD_ECO_MASTER')


if __name__ == '__main__':
    unittest.main()
