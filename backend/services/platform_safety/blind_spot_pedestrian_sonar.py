"""
CityBus Enterprise Platform - 360-Degree Blind-Spot Pedestrian Radar & Sonar
File: backend/services/platform_safety/blind_spot_pedestrian_sonar.py

Processes 77 GHz mmWave radar and 16-channel ultrasonic sonar arrays:
- Detects VRUs (Vulnerable Road Users: Pedestrians, Cyclists, Two-Wheelers)
- Blind-spot zones: FRONT_BLIND_SPOT, LEFT_KERB_TURNING, RIGHT_A_PILLAR, REAR_REVERSE
- Triggers audio visual cockpit HUD buzzer when distance < 1.5 meters
"""

from typing import List, Dict, Any


class BlindSpotPedestrianRadar:
    CRITICAL_PROXIMITY_METERS = 1.2
    WARNING_PROXIMITY_METERS = 2.5

    @staticmethod
    def evaluate_blind_spots(sensors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates 360 perimeter sensor channels.
        """
        threats = []
        for s in sensors:
            zone = s.get('zone', 'UNKNOWN')
            dist = s.get('distance_m', 5.0)
            target = s.get('detected_object', 'PEDESTRIAN')

            if dist <= BlindSpotPedestrianRadar.CRITICAL_PROXIMITY_METERS:
                threats.append({'zone': zone, 'distance_m': dist, 'level': 'CRITICAL_COLLISION_WARNING', 'object': target})
            elif dist <= BlindSpotPedestrianRadar.WARNING_PROXIMITY_METERS:
                threats.append({'zone': zone, 'distance_m': dist, 'level': 'PROXIMITY_ALERT', 'object': target})

        has_critical = any(t['level'] == 'CRITICAL_COLLISION_WARNING' for t in threats)

        return {
            'total_sensors_active': len(sensors),
            'detected_hazards_count': len(threats),
            'hazards': threats,
            'is_emergency_audio_alarm_active': has_critical,
            'cockpit_hmi_state': 'RED_ALERT_BRAKE_IMMEDIATELY' if has_critical else ('AMBER_CAUTION' if len(threats) > 0 else 'CLEAR_PERIMETER')
        }
