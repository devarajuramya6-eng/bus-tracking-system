"""
CityBus Enterprise Platform - Graph Router Unit Tests
File: tests/test_graph_router.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig
from models import db, Route, Stop, RouteStop
from services.graph_router import GraphRouterService


class TestGraphRouter(unittest.TestCase):
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

    def test_haversine_formula(self):
        dist = GraphRouterService.haversine_km(16.5062, 80.6480, 16.5120, 80.6500)
        self.assertGreater(dist, 0.5)
        self.assertLess(dist, 2.0)

    def test_find_itineraries_direct(self):
        stops = Stop.query.limit(2).all()
        if len(stops) >= 2:
            itineraries = GraphRouterService.find_itineraries(stops[0].id, stops[1].id)
            self.assertIsInstance(itineraries, list)


if __name__ == '__main__':
    unittest.main()
