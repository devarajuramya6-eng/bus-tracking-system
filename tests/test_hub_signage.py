"""
CityBus Enterprise Platform - Transit Hub Digital Signage Tests
File: tests/test_hub_signage.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.hub_signage.platform_bay_assignment_engine import PlatformBayAssigner
from services.hub_signage.multi_screen_split_renderer import MultiScreenDepartureRenderer
from services.hub_signage.accessibility_kiosk_hmi import AccessibilityKioskHMI


class TestHubSignage(unittest.TestCase):
    def test_platform_bay_assignment_nominal(self):
        bay = PlatformBayAssigner.assign_platform_bay(route_number="27A", bus_number="AP16-001", occupied_bays=[])
        self.assertEqual(bay['assigned_platform_bay'], 'BAY_04')
        self.assertFalse(bay['is_diverted_to_overflow'])

    def test_platform_bay_assignment_conflict_divert(self):
        bay = PlatformBayAssigner.assign_platform_bay(route_number="27A", bus_number="AP16-001", occupied_bays=['BAY_04'])
        self.assertNotEqual(bay['assigned_platform_bay'], 'BAY_04')
        self.assertTrue(bay['is_diverted_to_overflow'])

    def test_multi_screen_departure_board_json(self):
        deps = [{'route_number': '27A', 'destination_en': 'Guntur', 'eta_minutes': 1, 'bay': 'BAY_04'}]
        layout = MultiScreenDepartureRenderer.render_departure_board_json(deps)
        self.assertEqual(layout['total_departures_listed'], 1)
        self.assertEqual(layout['departures'][0]['status_label'], 'BOARDING NOW')

    def test_accessibility_kiosk_hmi(self):
        cfg = AccessibilityKioskHMI.get_kiosk_ui_config(is_wheelchair_mode=True, is_high_contrast=True)
        self.assertEqual(cfg['wheelchair_height_shift_px'], 280)
        self.assertEqual(cfg['color_theme'], 'HIGH_CONTRAST_YELLOW_ON_BLACK')


if __name__ == '__main__':
    unittest.main()
