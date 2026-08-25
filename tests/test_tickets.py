"""
CityBus Enterprise Platform - Ticketing & QR Cryptography Unit Tests
File: tests/test_tickets.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig
from models import db, User, Route
from services.ticket_service import TicketService


class TestTicketService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(name="Test Passenger", email="passenger@test.com", role="passenger")
        self.user.set_password("pass")
        self.user.save()

        self.route = Route(
            route_number="TEST-99",
            name="PNBS ⇄ Guntur Test",
            start_point="PNBS",
            destination="Guntur",
            base_fare=45.0
        )
        self.route.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fare_calculation_rules(self):
        # 10 km journey: 15.0 base + 10 * 1.5 = 30.0
        general = TicketService.calculate_fare(10.0, 1, 'general')
        self.assertEqual(general['total_fare'], 30.0)

        # Student 50% discount: 30 * 0.5 = 15.0
        student = TicketService.calculate_fare(10.0, 1, 'student')
        self.assertEqual(student['total_fare'], 15.0)

    def test_signed_qr_payload_generation_and_validation(self):
        ticket = TicketService.issue_ticket(
            user_id=self.user.id,
            route_id=self.route.id,
            origin="PNBS",
            destination="Guntur",
            fare_amount=45.0
        )
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.status, "VALID")

        # Validate with conductor
        val_ticket, status, msg = TicketService.validate_qr(ticket.qr_payload, conductor_id=1)
        self.assertEqual(status, "VALID")
        self.assertEqual(val_ticket.status, "USED")

        # Second validation should return ALREADY_USED
        val_ticket2, status2, msg2 = TicketService.validate_qr(ticket.qr_payload, conductor_id=1)
        self.assertEqual(status2, "ALREADY_USED")


if __name__ == '__main__':
    unittest.main()
