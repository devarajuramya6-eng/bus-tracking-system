"""
CityBus Enterprise Platform - Accessibility Deployment Warning Audio & Light Sync
File: backend/services/accessibility_ramp/driver_accessibility_chime.py

Controls exterior kerbside audio-visual warning signals during ramp movement:
- Exterior 75 dB pulsating warning chime (800 Hz tone, 2 Hz pulse rate)
- Flashing yellow door-sill LED light strip (warning boarding passengers)
- Cockpit HMI visual status synchronization
"""

from typing import Dict, Any


class AccessibilityDeploymentChime:
    @staticmethod
    def get_warning_signals(ramp_motion_state: str) -> Dict[str, Any]:
        """
        Calculates audio-visual warning parameters for ramp operations.
        """
        state = ramp_motion_state.upper().strip()
        is_moving = state in ('DEPLOYING', 'RETRACTING')

        if is_moving:
            buzzer = 'PULSATING_75DB_WARNING_CHIME'
            leds = 'FLASHING_AMBER_DOOR_SILL_LIGHTS'
        elif state == 'DEPLOYED':
            buzzer = 'SILENT'
            leds = 'STEADY_GREEN_BOARDING_LIGHTS'
        else:
            buzzer = 'SILENT'
            leds = 'OFF'

        return {
            'ramp_motion_state': state,
            'exterior_audible_buzzer': buzzer,
            'door_sill_lighting': leds,
            'is_passenger_caution_active': is_moving
        }
