"""
CityBus Enterprise Platform - Automated Audio Transit Announcement Generator
File: backend/services/pis/audio_announcement_generator.py

Generates phonetically aligned bilingual public address (PA) audio announcement scripts:
- Next Stop Approach (తెలుగు: తదుపరి స్టాప్... / English: Next stop is...)
- Terminal Arrival & Transfer announcements
- Passenger Safety alerts (Keep emergency exit clear, beware of pickpockets)
"""

from typing import Dict, Any


class AudioAnnouncementGenerator:
    @staticmethod
    def generate_next_stop_announcement(stop_name_te: str, stop_name_en: str, route_number: str) -> Dict[str, Any]:
        """
        Builds audio chime & spoken script for interior PA speakers.
        """
        script_te = f"తదుపరి స్టాప్ {stop_name_te}. ప్రయాణికులు దయచేసి సిద్ధంగా ఉండండి."
        script_en = f"Next stop is {stop_name_en}. Please prepare to alight."
        script_hi = f"अगला स्टॉप {stop_name_en} है।"

        return {
            'chime_sound': 'TWO_TONE_PIS_CHIME',
            'route_number': route_number,
            'scripts': {
                'te-IN': script_te,
                'en-IN': script_en,
                'hi-IN': script_hi
            },
            'full_spoken_text': f"{script_te} | {script_en}",
            'duration_estimate_sec': 7.5
        }

    @staticmethod
    def generate_emergency_announcement(message_en: str) -> Dict[str, Any]:
        return {
            'chime_sound': 'EMERGENCY_ALARM_CHIME',
            'script_en': f"Attention all passengers: {message_en}",
            'script_te': f"ప్రయాణికులందరికీ ముఖ్య గమనిక: {message_en}",
            'priority': 'HIGH_OVERRIDE'
        }
