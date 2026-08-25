"""
CityBus Enterprise Platform - Accessibility & ADA Unit Tests
File: tests/test_accessibility.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.accessibility.screen_reader_engine import AccessibilitySpeechEngine
from services.accessibility.wheelchair_space_reservation import WheelchairBayReservation
from services.accessibility.braille_signage_generator import TactileGuideGenerator


class TestAccessibilitySystems(unittest.TestCase):
    def test_screen_reader_audio_description(self):
        desc = AccessibilitySpeechEngine.generate_stop_accessibility_description(
            stop_name="Benz Circle",
            has_tactile_paving=True,
            has_shelter=True,
            platform_side="LEFT"
        )
        self.assertIn('speech_text_en', desc)
        self.assertIn('speech_text_te', desc)
        self.assertTrue(desc['has_tactile_paving'])
        self.assertEqual(desc['platform_door_side'], 'LEFT')

    def test_wheelchair_bay_reservation(self):
        res = WheelchairBayReservation.reserve_bay(
            user_id=202,
            passenger_name="S. Prasad",
            bus_id=101,
            route_number="27A",
            boarding_stop="PNBS",
            alighting_stop="Mangalagiri AIIMS"
        )
        self.assertEqual(res['status'], 'RESERVED_CONFIRMED')
        self.assertTrue(res['driver_assistance_required'])
        self.assertIn('♿', res['driver_hud_alert'])

    def test_braille_transliteration(self):
        braille = TactileGuideGenerator.text_to_braille("bus 27")
        self.assertIsInstance(braille, str)
        self.assertGreater(len(braille), 3)

        plaque = TactileGuideGenerator.generate_stop_plaque("PNBS", ["27A", "5K"])
        self.assertIn('braille_stop_name', plaque)
        self.assertIn('serving_routes', plaque)


if __name__ == '__main__':
    unittest.main()
