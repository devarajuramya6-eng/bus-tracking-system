"""
CityBus Enterprise Platform - Electronic Leveling Control (ELC) Pneumatic Kneeling
File: backend/services/air_suspension/pneumatic_kneeling_controller.py

Controls pneumatic solenoid valves on passenger entrance air springs (ECAS / ELC):
- Lowers right-side doorway sill height from 340 mm down to 270 mm (70 mm kneeling drop)
- Interspeed Lock: Kneeling only permitted when vehicle speed is 0.0 km/h and handbrake set
- Automatic recovery to normal ride height (340 mm) before vehicle drive-off
"""

from typing import Dict, Any


class ElectronicLevelingController:
    NORMAL_RIDE_HEIGHT_MM = 340.0
    KNEELED_RIDE_HEIGHT_MM = 270.0
    KNEELING_STROKE_MM = 70.0

    @staticmethod
    def execute_kneeling_command(command: str, vehicle_speed_kmh: float,
                                 is_handbrake_engaged: bool) -> Dict[str, Any]:
        """
        Processes ECAS kneeling / lift requests.
        """
        cmd = command.upper().strip()

        if cmd == 'KNEEL_RIGHT_DOORWAY':
            if vehicle_speed_kmh > 0.0 or not is_handbrake_engaged:
                return {
                    'success': False,
                    'error': 'Kneeling blocked: Vehicle must be stationary with handbrake engaged.',
                    'current_height_mm': ElectronicLevelingController.NORMAL_RIDE_HEIGHT_MM,
                    'is_kneeled': False
                }
            return {
                'success': True,
                'current_height_mm': ElectronicLevelingController.KNEELED_RIDE_HEIGHT_MM,
                'kneeling_drop_mm': ElectronicLevelingController.KNEELING_STROKE_MM,
                'is_kneeled': True,
                'solenoid_valve_state': 'RIGHT_BELLOWS_EXHAUST_OPEN',
                'status': 'VEHICLE_KNEELED_FOR_BOARDING'
            }

        elif cmd == 'RESTORE_RIDE_HEIGHT':
            return {
                'success': True,
                'current_height_mm': ElectronicLevelingController.NORMAL_RIDE_HEIGHT_MM,
                'kneeling_drop_mm': 0.0,
                'is_kneeled': False,
                'solenoid_valve_state': 'COMPRESSOR_RECHARGE_CLOSED',
                'status': 'NORMAL_DRIVING_HEIGHT_RESTORED'
            }

        return {'success': False, 'error': f"Unknown command {command}"}
