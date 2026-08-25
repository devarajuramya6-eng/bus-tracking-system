"""
CityBus Enterprise Platform - Driver Monitoring System (DMS) & Fatigue Detection
File: backend/services/safety/driver_fatigue_monitor.py

Processes in-cabin DMS AI camera telemetry:
- PERCLOS (Percentage of Eye Closure over 1-minute window)
- Micro-Sleep Events (Eyes closed > 1.5 seconds while vehicle in motion)
- Yawn frequency and head nodding posture angles
- Real-time in-cabin buzzer trigger and dispatcher alert
"""

from typing import Dict, Any, List


class DriverFatigueMonitor:
    PERCLOS_DROWSY_THRESHOLD = 0.22 # 22% closure triggers warning
    PERCLOS_CRITICAL_THRESHOLD = 0.35 # 35% closure triggers emergency stop

    @staticmethod
    def evaluate_fatigue_telemetry(bus_id: int, driver_id: int,
                                   speed_kmh: float,
                                   perclos_ratio: float,
                                   micro_sleep_duration_sec: float,
                                   yawns_last_5min: int) -> Dict[str, Any]:
        """
        Assesses driver alertness state.
        """
        is_moving = speed_kmh > 5.0

        if is_moving and (micro_sleep_duration_sec >= 1.5 or perclos_ratio >= DriverFatigueMonitor.PERCLOS_CRITICAL_THRESHOLD):
            return {
                'bus_id': bus_id,
                'driver_id': driver_id,
                'alert_level': 'CRITICAL_FATIGUE_EMERGENCY',
                'cockpit_buzzer': True,
                'haptic_seat_vibration': True,
                'dispatch_alert': True,
                'perclos': round(perclos_ratio, 3),
                'micro_sleep_sec': micro_sleep_duration_sec,
                'action_required': 'MANDATORY_RELIEF_STOP_REQUIRED',
                'message': f"CRITICAL: Driver microsleep of {micro_sleep_duration_sec:.1f}s detected on Bus {bus_id} at {speed_kmh:.1f} km/h!"
            }

        elif perclos_ratio >= DriverFatigueMonitor.PERCLOS_DROWSY_THRESHOLD or yawns_last_5min >= 4:
            return {
                'bus_id': bus_id,
                'driver_id': driver_id,
                'alert_level': 'WARNING_DROWSINESS',
                'cockpit_buzzer': True,
                'haptic_seat_vibration': False,
                'dispatch_alert': False,
                'perclos': round(perclos_ratio, 3),
                'micro_sleep_sec': micro_sleep_duration_sec,
                'action_required': 'AUDIO_ALERT_CHIME',
                'message': f"Drowsiness advisory: Increased blink/yawn rate detected for Driver {driver_id}."
            }

        return {
            'bus_id': bus_id,
            'driver_id': driver_id,
            'alert_level': 'NOMINAL_ALERT',
            'cockpit_buzzer': False,
            'haptic_seat_vibration': False,
            'dispatch_alert': False,
            'perclos': round(perclos_ratio, 3),
            'action_required': 'NONE'
        }
