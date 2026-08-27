"""
CityBus Enterprise Platform - Passenger Information System (PIS) & Audio Engine
File: backend/services/passenger_information_service.py

Generates multilingual audio announcements (English, Telugu, Hindi),
formats LED destination scroll boards, and broadcasts platform RTPI feeds.
"""

from typing import Dict, List, Any, Optional
from models import Route, Stop, Bus, db


class PassengerInformationService:
    """Manages audio/visual PIS feeds and LED destination board formatting."""

    DESTINATION_SIGNS = {
        "27A": {"en": "27A PNBS <-> GUNTUR EXP", "te": "27A పి.ఎన్.బి.ఎస్ - గుంటూరు", "code": "EXP-27A"},
        "5A":  {"en": "5A AIRPORT EXPRESS", "te": "5A గన్నవరం విమానాశ్రయం", "code": "AIR-05A"},
        "10H": {"en": "10H AIIMS METRO FEEDER", "te": "10H ఎయిమ్స్ ఫీడర్", "code": "MET-10H"},
        "12B": {"en": "12B BENZ CIRCLE LOCAL", "te": "12B బెంజ్ సర్కిల్", "code": "LOC-12B"}
    }

    @classmethod
    def get_destination_led_sign(cls, route_number: str) -> Dict[str, Any]:
        """Returns formatted LED sign text and Telugu translation matrix."""
        clean_num = route_number.strip().upper()
        sign = cls.DESTINATION_SIGNS.get(clean_num, {
            "en": f"{clean_num} CITYBUS TRANSIT",
            "te": f"{clean_num} సిటీ బస్సు",
            "code": f"BUS-{clean_num}"
        })

        return {
            "route_number": clean_num,
            "led_line_1_english": sign["en"],
            "led_line_2_telugu": sign["te"],
            "led_color": "#FFCC00", # High visibility amber LED
            "matrix_resolution": "192x32",
            "scroll_mode": "CONTINUOUS_MARQUEE"
        }

    @classmethod
    def generate_stop_announcements(cls, stop_name: str, next_stop_name: Optional[str] = None) -> Dict[str, Any]:
        """Generates trilingual audio announcement transcript scripts."""
        return {
            "stop_name": stop_name,
            "next_stop_name": next_stop_name,
            "audio_scripts": {
                "english": {
                    "approaching": f"Next stop is {stop_name}. Please prepare to alight.",
                    "arrived": f"Now arriving at {stop_name}. Mind the platform gap."
                },
                "telugu": {
                    "approaching": f"తదుపరి స్టాప్ {stop_name}.",
                    "arrived": f"{stop_name} చేరుకున్నాము."
                },
                "hindi": {
                    "approaching": f"अगला स्टॉप {stop_name} है।",
                    "arrived": f"अब हम {stop_name} पहुंच चुके हैं।"
                }
            },
            "chime_type": "DUAL_TONE_PIS_CHIME"
        }
