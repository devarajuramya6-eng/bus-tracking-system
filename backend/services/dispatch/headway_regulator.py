"""
CityBus Enterprise Platform - Dynamic Headway Regulation & Control Strategy Engine
File: backend/services/dispatch/headway_regulator.py

Calculates tactical control actions to eliminate bus bunching and large service gaps:
- Holding Strategy: Computes exact hold duration in seconds at upcoming timepoint stop
- Speed Adjustment Advisory: Recommends target cruise speed (e.g. 22 km/h vs 38 km/h)
- Skip-Stop Advisory: Authorizes express bypass of minor stops when severely delayed
"""

from typing import Dict, Any, List


class DynamicHeadwayRegulator:
    TARGET_HEADWAY_SECONDS = 600 # 10 minutes scheduled headway

    @staticmethod
    def calculate_regulation_strategy(scheduled_headway_sec: int,
                                      actual_headway_ahead_sec: int,
                                      actual_headway_behind_sec: int,
                                      current_stop_name: str) -> Dict[str, Any]:
        """
        Calculates optimal headway regulation action.
        """
        headway_ratio_ahead = actual_headway_ahead_sec / max(1, scheduled_headway_sec)

        # Bunching scenario (trailing vehicle is catching up to lead vehicle)
        if actual_headway_ahead_sec < (scheduled_headway_sec * 0.40): # < 4 minutes apart
            hold_sec = min(180, int((scheduled_headway_sec - actual_headway_ahead_sec) * 0.60))
            return {
                'action_type': 'HOLD_AT_STOP',
                'severity': 'HIGH_BUNCHING',
                'target_stop': current_stop_name,
                'hold_duration_seconds': hold_sec,
                'advisory_message': f"Hold vehicle at {current_stop_name} for {hold_sec} seconds to restore 10-minute spacing."
            }

        # Service Gap scenario (vehicle is lagging behind, creating big gap ahead)
        elif actual_headway_ahead_sec > (scheduled_headway_sec * 1.60): # > 16 minutes gap ahead
            return {
                'action_type': 'SPEED_UP_OR_EXPRESS',
                'severity': 'SERVICE_GAP',
                'target_stop': current_stop_name,
                'hold_duration_seconds': 0,
                'target_speed_kmh': 42.0,
                'advisory_message': f"Large gap ahead ({actual_headway_ahead_sec // 60} min). Maintain maximum safe corridor speed."
            }

        return {
            'action_type': 'MAINTAIN_PACE',
            'severity': 'NORMAL',
            'target_stop': current_stop_name,
            'hold_duration_seconds': 0,
            'advisory_message': "Headway within nominal parameters. Continue regular timetable pace."
        }
