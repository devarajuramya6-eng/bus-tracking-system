"""
CityBus Enterprise Platform - Origin-Destination (OD) Analytics Tests
File: tests/test_od_analytics.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.od_analytics.bilevel_od_inversion import BiLevelODInversion
from services.od_analytics.transfer_matrix_calculator import TransferMatrixCalculator
from services.od_analytics.station_dwell_time_ml import StationDwellTimePredictor


class TestODAnalytics(unittest.TestCase):
    def test_bilevel_od_inversion_balancing(self):
        boardings = [100, 50, 0]
        alightings = [0, 60, 90]
        dist_matrix = [[0.0, 5.0, 10.0], [0.0, 0.0, 5.0], [0.0, 0.0, 0.0]]
        od = BiLevelODInversion.balance_od_matrix(boardings, alightings, dist_matrix)
        self.assertEqual(len(od), 3)
        self.assertAlmostEqual(sum(od[0]), 100.0, delta=5.0)

    def test_transfer_matrix_calculator(self):
        taps = [
            {'card_id': 1, 'route_num': '27A', 'timestamp_sec': 1000},
            {'card_id': 1, 'route_num': '5K', 'timestamp_sec': 1900}, # Transfer (< 2700s)
            {'card_id': 2, 'route_num': '10', 'timestamp_sec': 1200}  # Direct
        ]
        res = TransferMatrixCalculator.calculate_hub_transfers(taps)
        self.assertEqual(res['transfer_linked_trips'], 1)
        self.assertEqual(res['direct_single_trips'], 2)

    def test_station_dwell_time_ml(self):
        dwell = StationDwellTimePredictor.predict_dwell_time(boardings_count=15, alightings_count=10, smart_card_ratio=0.8)
        self.assertGreater(dwell['estimated_dwell_seconds'], 10.0)
        self.assertLess(dwell['estimated_dwell_seconds'], 60.0)


if __name__ == '__main__':
    unittest.main()
