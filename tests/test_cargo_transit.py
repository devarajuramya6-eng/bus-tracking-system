"""
CityBus Enterprise Platform - Freight on Transit & Smart Lockers Tests
File: tests/test_cargo_transit.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.cargo_transit.passenger_bus_belly_freight import BellyFreightAllocator
from services.cargo_transit.station_smart_locker_grid import SmartLockerGridManager
from services.cargo_transit.parcel_chain_of_custody import ParcelChainOfCustodyTracker


class TestCargoTransit(unittest.TestCase):
    def test_belly_freight_allocation(self):
        alloc = BellyFreightAllocator.allocate_cargo_consignment(
            bus_id=1,
            bus_number="AP16-001",
            current_loaded_weight_kg=120.0,
            parcel_weight_kg=15.0,
            parcel_volume_m3=0.08
        )
        self.assertTrue(alloc['is_shipment_accepted'])
        self.assertEqual(alloc['status'], 'BOOKED_FOR_TRANSIT')
        self.assertGreater(alloc['freight_charge_inr'], 40.0)

    def test_smart_locker_box_assignment(self):
        locker = SmartLockerGridManager.assign_locker_box("PNBS-01", "PKG-9821")
        self.assertIn('BOX-', locker['allocated_box_number'])
        self.assertEqual(len(locker['pickup_pin_otp']), 6)

    def test_parcel_chain_of_custody(self):
        event = ParcelChainOfCustodyTracker.record_handover_event(
            parcel_id="PKG-9821",
            event_type="LOADED_ON_BUS",
            handler_employee_id=102,
            bus_or_station_id="BUS-AP16-001",
            lat=16.5062,
            lng=80.6480
        )
        self.assertTrue(event['is_custody_verified'])
        self.assertEqual(event['custody_event'], 'LOADED_ON_BUS')


if __name__ == '__main__':
    unittest.main()
