"""
CityBus Enterprise Platform - Incidents & Emergency SOS Unit Tests
File: tests/test_incidents.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig
from models import db, Bus, Incident
from services.incident_service import IncidentService
from repositories.incident_repository import IncidentRepository


class TestIncidentService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.bus = Bus(bus_number="AP16-101", status="On Route")
        self.bus.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_incident_reporting_and_kanban_transition(self):
        inc = IncidentService.report_incident(
            incident_type="Breakdown",
            title="Radiator Overheat",
            description="High temperature warning",
            severity="Medium",
            bus_id=self.bus.id
        )
        self.assertEqual(inc.status, "New")

        updated = IncidentRepository.update_incident_status(inc.id, "In Progress", resolution_notes="Technician dispatched")
        self.assertEqual(updated.status, "In Progress")

    def test_emergency_sos_panic_trigger(self):
        inc = IncidentService.trigger_emergency_sos(
            bus_id=self.bus.id,
            driver_id=1,
            lat=16.5062,
            lng=80.6480
        )
        self.assertEqual(inc.severity, "Critical")
        
        # Verify bus status was escalated to Emergency
        b = Bus.query.get(self.bus.id)
        self.assertEqual(b.status, "Emergency")


if __name__ == '__main__':
    unittest.main()
