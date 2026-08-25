"""
CityBus Enterprise Platform - Destination LED Sign Matrix Tests
File: tests/test_destination_led.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.destination_led.led_matrix_framebuffer import LEDMatrixFramebuffer
from services.destination_led.route_code_lookup import DestinationRouteCodeLookup
from services.destination_led.bilingual_glyph_renderer import BilingualGlyphRenderer


class TestDestinationLED(unittest.TestCase):
    def test_led_framebuffer_generation(self):
        fb = LEDMatrixFramebuffer.render_text_framebuffer("27A", "GUNTUR EXP")
        self.assertEqual(fb['matrix_width'], 128)
        self.assertEqual(fb['matrix_height'], 16)
        self.assertEqual(fb['total_led_pixels'], 2048)
        self.assertIn('binary_payload_hex', fb)

    def test_route_code_lookup(self):
        code_data = DestinationRouteCodeLookup.lookup_route_code(127)
        self.assertEqual(code_data['status'], 'CODE_FOUND')
        self.assertIn('27A GUNTUR BUS STATION', code_data['front_sign'])
        self.assertIn('గుంటూరు', code_data['front_sign_te'])

    def test_bilingual_glyph_renderer(self):
        res = BilingualGlyphRenderer.render_bilingual_header("27A", "Guntur", "గుంటూరు")
        self.assertEqual(res['route_badge'], '27A')
        self.assertTrue(res['is_bilingual_certified'])
        self.assertEqual(res['slide_duration_seconds'], 3.5)


if __name__ == '__main__':
    unittest.main()
