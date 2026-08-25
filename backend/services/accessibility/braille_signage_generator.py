"""
CityBus Enterprise Platform - Tactile Braille Transit Signage Generator
File: backend/services/accessibility/braille_signage_generator.py

Converts alphanumeric transit route information into Unicode Braille patterns (U+2800 to U+28FF):
- Generates tactile plaque layouts for bus stop flag poles
- Unified English Braille (UEB) Grade 1 transliteration
"""

from typing import Dict, Any


class TactileGuideGenerator:
    BRAILLE_MAP = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
        'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
        'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
        '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
        '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚',
        ' ': ' ', '-': '⠤', '.': '⠲', ':': '⠒'
    }

    @staticmethod
    def text_to_braille(text: str) -> str:
        """Transliterates text string into Unicode Braille dot characters."""
        lower_text = text.lower()
        result = []
        for ch in lower_text:
            result.append(TactileGuideGenerator.BRAILLE_MAP.get(ch, ''))
        return "".join(result)

    @staticmethod
    def generate_stop_plaque(stop_name: str, route_numbers: list) -> Dict[str, Any]:
        """
        Builds tactile stop signage with Braille patterns.
        """
        braille_stop = TactileGuideGenerator.text_to_braille(stop_name)
        routes_str = ", ".join(route_numbers)
        braille_routes = TactileGuideGenerator.text_to_braille(routes_str)

        return {
            'stop_name': stop_name,
            'braille_stop_name': braille_stop,
            'serving_routes': route_numbers,
            'braille_routes': braille_routes,
            'contrast_ratio': '21:1_BLACK_ON_YELLOW',
            'dimensions_mm': {'width': 200, 'height': 300, 'emboss_height_mm': 0.8}
        }
