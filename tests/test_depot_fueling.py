"""
CityBus Enterprise Platform - Depot Automated Fuel Dispensing Tests
File: tests/test_depot_fueling.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.depot_fueling.rfid_nozzle_interlock import RFIDFuelNozzleInterlock
from services.depot_fueling.fuel_flowmeter_pulsar_telemetry import FlowMeterPulsarTelemetry
from services.depot_fueling.def_adblue_metering_tracker import DEFAdBlueMeteringTracker


class TestDepotFueling(unittest.TestCase):
    def test_rfid_nozzle_authorization_valid(self):
        auth = RFIDFuelNozzleInterlock.verify_nozzle_insertion(
            scanned_rfid_tag="RFID_AP16_001",
            is_nozzle_seated=True
        )
        self.assertTrue(auth['dispense_authorized'])
        self.assertEqual(auth['solenoid_valve_state'], 'SOLENOID_VALVE_OPEN_DISPENSE')

    def test_rfid_nozzle_authorization_unseated(self):
        auth = RFIDFuelNozzleInterlock.verify_nozzle_insertion(
            scanned_rfid_tag="RFID_AP16_001",
            is_nozzle_seated=False
        )
        self.assertFalse(auth['dispense_authorized'])
        self.assertEqual(auth['solenoid_valve_state'], 'SOLENOID_CLOSED_NOZZLE_WITHDRAWN')

    def test_flowmeter_pulsar_calculation(self):
        flow = FlowMeterPulsarTelemetry.calculate_dispensed_liters(
            pulse_count=12000, # 120.0 Liters
            duration_seconds=120.0
        )
        self.assertEqual(flow['dispensed_volume_liters'], 120.0)
        self.assertEqual(flow['dispense_flow_rate_lpm'], 60.0)
        self.assertTrue(flow['is_high_speed_commercial_flow'])

    def test_def_adblue_dosing_audit(self):
        audit = DEFAdBlueMeteringTracker.audit_def_dosing(
            bus_number="AP16-001",
            diesel_burned_liters=100.0,
            def_consumed_liters=5.0, # 5.0%
            urea_refractometer_pct=32.5
        )
        self.assertTrue(audit['is_bs6_emissions_compliant'])
        self.assertEqual(audit['def_dosing_ratio_pct'], 5.0)


if __name__ == '__main__':
    unittest.main()
