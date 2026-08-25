"""
CityBus Enterprise Platform - BRT Station Express Overtaking Coordinator
File: backend/services/headway_platooning/express_overtaking_coordinator.py

Coordinates express bus overtaking maneuvers at 4-track bypass BRT stations:
- Express Bus (Non-stop) bypasses Local Bus (Dwell exchange at platform)
- Verifies passing lane clear zone via station lidar/cctv sensors
- Emits digital signal clearance to cockpit HUD (GREEN_BYPASS_AUTHORIZED)
"""

from typing import Dict, Any


class ExpressOvertakingCoordinator:
    @staticmethod
    def evaluate_overtake_clearance(express_bus_number: str,
                                    local_bus_number: str,
                                    station_id: str,
                                    passing_lane_clear: bool,
                                    local_bus_stationary: bool) -> Dict[str, Any]:
        """
        Grants electronic authorization for overtaking maneuver.
        """
        is_safe_to_pass = passing_lane_clear and local_bus_stationary

        return {
            'express_bus_number': express_bus_number,
            'local_bus_number': local_bus_number,
            'station_id': station_id,
            'passing_lane_obstruction_free': passing_lane_clear,
            'local_bus_dwell_confirmed': local_bus_stationary,
            'overtake_authorization': 'GREEN_BYPASS_AUTHORIZED' if is_safe_to_pass else 'HOLD_BEHIND_LOCAL_BUS',
            'is_passing_safe': is_safe_to_pass
        }
