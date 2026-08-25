"""
CityBus Enterprise Platform - Universal Accessibility & Screen Reader Audio Engine
File: backend/services/accessibility/screen_reader_engine.py

Generates phonetically descriptive audio guidance for visually impaired and elderly commuters:
- Platform tactile paving path descriptions
- Low-floor bus kneeling & manual fold-out ramp deployment notifications
- Acoustic wayfinding beacon triggering (Bluetooth Low Energy BLE audio chirp)
"""

from typing import Dict, Any, List


class AccessibilitySpeechEngine:
    @staticmethod
    def generate_stop_accessibility_description(stop_name: str, has_tactile_paving: bool, has_shelter: bool, platform_side: str = "LEFT") -> Dict[str, Any]:
        """
        Builds audio description for a bus stop.
        """
        paving_text = "Tactile paving guide strip is installed from sidewalk to boarding curb." if has_tactile_paving else "Caution: No tactile guide path on this curb."
        shelter_text = "Covered passenger waiting shelter with audio announcement speaker is present." if has_shelter else "Open curb stop without canopy shelter."

        speech_text = f"You are at {stop_name}. Doors will open on the {platform_side.lower()} side. {paving_text} {shelter_text}"

        return {
            'stop_name': stop_name,
            'speech_text_en': speech_text,
            'speech_text_te': f"మీరు {stop_name} వద్ద ఉన్నారు. తలుపులు {platform_side} వైపు తెరవబడతాయి.",
            'has_tactile_paving': has_tactile_paving,
            'has_shelter': has_shelter,
            'platform_door_side': platform_side,
            'audio_beacon_frequency_hz': 880,
            'aria_label': f"Transit stop: {stop_name}, Door opening: {platform_side}"
        }
