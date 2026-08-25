"""
CityBus Enterprise Platform - GTFS Export Engine Unit Tests
File: tests/test_gtfs.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig
from models import db
from services.gtfs_exporter import GTFSExportService


class TestGTFSExport(unittest.TestCase):
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

    def test_generate_agency_txt(self):
        txt = GTFSExportService.generate_agency_txt()
        self.assertIn('agency_id', txt)
        self.assertIn('APSRTC_VJA', txt)

    def test_generate_gtfs_zip(self):
        zip_bytes = GTFSExportService.generate_gtfs_zip_bytes()
        self.assertGreater(len(zip_bytes), 100)


if __name__ == '__main__':
    unittest.main()
