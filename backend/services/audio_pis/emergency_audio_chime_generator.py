"""
CityBus Enterprise Platform - ISO 7731 Transit Auditory Warning Chime Generator
File: backend/services/audio_pis/emergency_audio_chime_generator.py

Generates ISO 7731 compliant audio chime tone frequencies and durations:
- DOOR_CLOSING_CHIME: Two-tone chime (880 Hz ➔ 440 Hz)
- NEXT_STOP_PING: Single ascending chime (587 Hz ➔ 880 Hz)
- EMERGENCY_ALARM_TONE: Rapid pulsing warble (1200 Hz - 1800 Hz)
"""

from typing import Dict, Any, List


class EmergencyAudioChimeGenerator:
    CHIME_PRESETS = {
        'DOOR_CLOSING': {
            'name': 'Two-Tone Door Closing Chime',
            'frequencies_hz': [880, 440],
            'durations_ms': [250, 400],
            'gap_ms': 50
        },
        'NEXT_STOP': {
            'name': 'Ascending Station Arrival Ding',
            'frequencies_hz': [587, 880],
            'durations_ms': [200, 300],
            'gap_ms': 40
        },
        'EMERGENCY_ALARM': {
            'name': 'Rapid SOS Evacuation Warble',
            'frequencies_hz': [1200, 1800, 1200, 1800],
            'durations_ms': [150, 150, 150, 150],
            'gap_ms': 20
        }
    }

    @staticmethod
    def get_chime_config(chime_type: str) -> Dict[str, Any]:
        """
        Retrieves chime sequence definition.
        """
        preset = EmergencyAudioChimeGenerator.CHIME_PRESETS.get(chime_type, EmergencyAudioChimeGenerator.CHIME_PRESETS['NEXT_STOP'])
        return {
            'chime_type': chime_type,
            'preset_name': preset['name'],
            'frequencies_hz': preset['frequencies_hz'],
            'durations_ms': preset['durations_ms'],
            'sample_rate_hz': 44100
        }
