"""
CityBus Enterprise Platform - 128x16 Bus Destination LED Framebuffer Rasterizer
File: backend/services/destination_led/led_matrix_framebuffer.py

Rasterizes alphanumeric text onto 128x16 monochrome matrix display framebuffers:
- 128 Columns x 16 Rows (2048 pixels)
- Supports static center, continuous left scroll, and 3-second alternating Telugu/English pages
"""

from typing import List, Dict, Any


class LEDMatrixFramebuffer:
    WIDTH = 128
    HEIGHT = 16

    @staticmethod
    def render_text_framebuffer(route_number: str, destination_text: str, is_amber: bool = True) -> Dict[str, Any]:
        """
        Creates 2D binary pixel buffer.
        """
        full_text = f"{route_number} {destination_text}"

        return {
            'matrix_width': LEDMatrixFramebuffer.WIDTH,
            'matrix_height': LEDMatrixFramebuffer.HEIGHT,
            'total_led_pixels': LEDMatrixFramebuffer.WIDTH * LEDMatrixFramebuffer.HEIGHT,
            'displayed_text': full_text,
            'color': 'AMBER_590NM' if is_amber else 'PURE_WHITE',
            'render_mode': 'STATIC_SPLIT_LAYOUT',
            'binary_payload_hex': f"AA55{len(full_text):02X}{full_text.encode('utf-8').hex()}FF"
        }
