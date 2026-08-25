"""
CityBus Enterprise Platform - Bus & Telemetry Unit Tests
File: tests/test_buses.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig
from models import db, Bus, Route
from services.gps_service import GPSService
from repositories.bus_repository import BusRepository


class TestBusService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed sample bus
        self.bus = Bus(
            bus_number="AP16-999",
            model="Electric AC Low Floor",
            latitude=16.5062,
            longitude=80.6480,
            speed=35.0,
            status="On Route"
        )
        self.bus.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_haversine_distance_calculation(self):
        # Distance between PNBS (16.5100, 80.6175) and Benz Circle (16.5020, 80.6475) is approx 3.3 km
        dist = BusRepository.haversine_km(16.5100, 80.6175, 16.5020, 80.6475)
        self.assertAlmostEqual(dist, 3.3, delta=0.5)

    def test_gps_telemetry_ingestion(self):
        res, err = GPSService.process_telemetry_ping(self.bus.id, 16.5120, 80.6500, speed=42.0)
        self.assertIsNone(err)
        self.assertEqual(res['bus']['latitude'], 16.5120)
        self.assertEqual(res['bus']['speed'], 42.0)

    def test_nearby_buses_api(self):
        response = self.client.get('/api/v1/buses/nearby?lat=16.5060&lng=80.6480&radius_km=5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 1)


if __name__ == '__main__':
    unittest.main()
