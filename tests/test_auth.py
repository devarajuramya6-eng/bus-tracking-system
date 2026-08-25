"""
CityBus Enterprise Platform - Authentication & RBAC Unit Tests
File: tests/test_auth.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig
from models import db, User
from services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        import time
        user = User(name="Test Passenger", email=f"test_{int(time.time()*1000)}@citybus.transit", role="passenger")
        user.set_password("secure_pass_123")
        self.assertTrue(user.check_password("secure_pass_123"))
        self.assertFalse(user.check_password("wrong_password"))

    def test_jwt_token_generation_and_verification(self):
        import time
        user = User(name="Test Driver", email=f"driver_{int(time.time()*1000)}@citybus.transit", role="driver")
        user.set_password("citybus2026")
        user.save()

        tokens = AuthService.generate_tokens(user)
        self.assertIn('access_token', tokens)
        self.assertIn('refresh_token', tokens)

        payload = AuthService.verify_token(tokens['access_token'])
        self.assertIsNotNone(payload)
        self.assertEqual(payload['sub'], str(user.id))
        self.assertEqual(payload['role'], 'driver')

    def test_auth_login_endpoint(self):
        import time
        unique_email = f"auth_{int(time.time()*1000)}@citybus.transit"
        user = User(name="Auth Test", email=unique_email, role="passenger")
        user.set_password("password123")
        user.save()

        response = self.client.post('/api/v1/auth/login', json={
            'email': unique_email,
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('access_token', data)


if __name__ == '__main__':
    unittest.main()
