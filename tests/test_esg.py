"""
CityBus Enterprise Platform - ESG Sustainability & Carbon Footprint Tests
File: tests/test_esg.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.esg.carbon_emissions_calculator import CarbonEmissionsCalculator
from services.esg.passenger_green_points import PassengerGreenPointsLedger
from services.esg.esg_sustainability_report import ESGSustainabilityReportGenerator


class TestESGSustainability(unittest.TestCase):
    def test_fleet_carbon_emissions_calculation(self):
        emissions = CarbonEmissionsCalculator.calculate_fleet_emissions(
            diesel_fleet_km=10000.0,
            electric_fleet_km=8000.0
        )
        self.assertGreater(emissions['diesel_scope1_co2_tonnes'], 0.0)
        self.assertGreater(emissions['co2_avoided_by_ev_tonnes'], 0.0)
        self.assertGreater(emissions['trees_planted_equivalent'], 0)

    def test_passenger_green_points_award(self):
        points = PassengerGreenPointsLedger.award_trip_points(user_id=1, distance_km=12.5, is_electric_bus=True)
        self.assertGreater(points['green_points_earned'], 5)
        self.assertIn('co2_avoided_kg', points)

    def test_esg_quarterly_report_generation(self):
        report = ESGSustainabilityReportGenerator.generate_quarterly_report("Q3-2026")
        self.assertEqual(report['reporting_period'], 'Q3-2026')
        self.assertGreater(report['diesel_fuel_displaced_liters'], 1000.0)
        self.assertEqual(report['compliance_certification'], 'ISO_14064_GREENHOUSE_GAS_VERIFIED')


if __name__ == '__main__':
    unittest.main()
