"""
CityBus Enterprise Platform - Demand & Crowding Forecasting Unit Tests
File: tests/test_demand_forecasting.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.forecasting.passenger_demand_arima import PassengerDemandForecaster
from services.forecasting.dynamic_fleet_allocator import DynamicFleetAllocator
from services.forecasting.crowding_prediction_model import CrowdingPredictionModel


class TestDemandForecasting(unittest.TestCase):
    def test_passenger_demand_forecasting(self):
        forecast = PassengerDemandForecaster.forecast_daily_demand(
            route_id=1,
            base_daily_ridership=10000,
            is_rainy=True
        )
        self.assertEqual(len(forecast['hourly_breakdown']), 24)
        self.assertGreater(forecast['total_forecasted_ridership'], 10000) # Rain multiplier

    def test_dynamic_fleet_allocation(self):
        alloc = DynamicFleetAllocator.calculate_fleet_requirement(
            route_id=1,
            route_number="27A",
            peak_hourly_demand=450,
            round_trip_duration_min=90
        )
        self.assertGreater(alloc['required_operating_buses'], 5)
        self.assertGreaterEqual(alloc['recommended_reserve_buses'], 1)

    def test_crowding_prediction_model(self):
        crowd = CrowdingPredictionModel.predict_trip_crowding(departure_hour=8, is_school_working_day=True)
        self.assertIn(crowd['crowding_level'], ['STANDING_ROOM_ONLY', 'FEW_SEATS_AVAILABLE', 'SEATS_AVAILABLE'])
        self.assertGreater(crowd['expected_occupancy_pct'], 70.0)


if __name__ == '__main__':
    unittest.main()
