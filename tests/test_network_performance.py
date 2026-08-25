"""
CityBus Enterprise Platform - Network Performance & OTP Unit Tests
File: tests/test_network_performance.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.network_performance.otp_service_metrics import OnTimePerformanceEngine
from services.network_performance.excess_wait_time_ewt import ExcessWaitTimeCalculator
from services.network_performance.route_profitability_matrix import RouteProfitabilityAnalyzer


class TestNetworkPerformance(unittest.TestCase):
    def test_on_time_performance_metrics(self):
        trips = [
            {'delay_minutes': 0.0},
            {'delay_minutes': 2.0},
            {'delay_minutes': 4.0},
            {'delay_minutes': 8.0} # 1 Late, 3 On-time (75%)
        ]
        otp = OnTimePerformanceEngine.calculate_route_otp(trips)
        self.assertEqual(otp['total_trips_evaluated'], 4)
        self.assertEqual(otp['on_time_trips'], 3)
        self.assertEqual(otp['otp_compliance_percentage'], 75.0)

    def test_excess_wait_time_calculator(self):
        scheduled = [10.0, 10.0, 10.0, 10.0]
        actual = [4.0, 16.0, 5.0, 15.0] # Bunching
        ewt = ExcessWaitTimeCalculator.calculate_ewt(scheduled, actual)
        self.assertGreater(ewt['excess_wait_time_min'], 0.0)
        self.assertGreater(ewt['actual_wait_time_min'], ewt['scheduled_wait_time_min'])

    def test_route_profitability_economics(self):
        econ = RouteProfitabilityAnalyzer.evaluate_route_economics(
            route_number="27A",
            total_revenue_inr=15000.0,
            total_distance_km=250.0,
            is_electric=True
        )
        self.assertEqual(econ['earnings_per_km_epkm'], 60.0)
        self.assertGreater(econ['net_profit_or_loss_inr'], 0.0)
        self.assertEqual(econ['commercial_viability'], 'PROFITABLE_COMMERCIAL')


if __name__ == '__main__':
    unittest.main()
