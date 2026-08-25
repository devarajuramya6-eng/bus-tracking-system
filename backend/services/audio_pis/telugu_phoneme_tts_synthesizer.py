"""
CityBus Enterprise Platform - Telugu & English Phonetic PIS Audio Generator
File: backend/services/audio_pis/telugu_phoneme_tts_synthesizer.py

Synthesizes high-fidelity bilingual audio announcements for in-bus public address (PA):
- Generates W3C SSML (Speech Synthesis Markup Language) audio payloads
- Telugu announcements: "తదుపరి స్టాప్ బెంజ్ సర్కిల్. దిగే ప్రయాణికులు సిద్ధంగా ఉండండి."
- English announcements: "Next Stop: Benz Circle. Change here for Metro Feeder Buses."
"""

from typing import Dict, Any


class TeluguAudioTTSSynthesizer:
    @staticmethod
    def generate_next_stop_ssml(stop_name_en: str, stop_name_te: str,
                                interchange_routes: str = "") -> Dict[str, Any]:
        """
        Builds bilingual SSML announcement payload.
        """
        interchange_te = f" ఇక్కడ {interchange_routes} బస్సులకు మారవచ్చు." if interchange_routes else ""
        interchange_en = f" Change here for {interchange_routes}." if interchange_routes else ""

        ssml_telugu = f'<speak><voice name="te-IN-MohanNeural"><prosody rate="0.95">తదుపరి స్టాప్: {stop_name_te}.{interchange_te}</prosody></voice></speak>'
        ssml_english = f'<speak><voice name="en-IN-PrabhatNeural"><prosody rate="1.0">Next Stop: {stop_name_en}.{interchange_en}</prosody></voice></speak>'

        return {
            'stop_name_en': stop_name_en,
            'stop_name_te': stop_name_te,
            'ssml_telugu': ssml_telugu,
            'ssml_english': ssml_english,
            'audio_format': 'AUDIO_16KHZ_128KBIT_MP3',
            'interchange_available': bool(interchange_routes)
        }
