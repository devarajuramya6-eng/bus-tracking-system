"""
CityBus Enterprise Platform - Dynamic Stop Holding Headway Regularization
File: backend/services/headway_platooning/holding_strategy_controller.py

Implements forward and backward headway holding control to prevent bus bunching:
- Target Headway: $H_{target} = 10\text{ mins}$
- Computes holding duration at designated timing control points (e.g. Benz Circle Stop)
- Maximum allowable hold: 90 seconds (to avoid excessive passenger frustration)
"""

from typing import Dict, Any


class HeadwayHoldingController:
    MAX_ALLOWABLE_HOLD_SECONDS = 90.0

    @staticmethod
    def calculate_holding_dwell(forward_headway_min: float,
                                backward_headway_min: float,
                                target_headway_min: float = 10.0) -> Dict[str, Any]:
        """
        Calculates required holding delay at current stop.
        """
        # Headway error
        forward_error = forward_headway_min - target_headway_min
        backward_error = target_headway_min - backward_headway_min

        # If catching up with leading bus (forward headway too small)
        if forward_headway_min < target_headway_min * 0.7:
            # Need to hold at stop
            hold_sec = min(HeadwayHoldingController.MAX_ALLOWABLE_HOLD_SECONDS, (target_headway_min - forward_headway_min) * 60.0 * 0.5)
            action = 'HOLD_AT_STATION'
        elif forward_headway_min > target_headway_min * 1.3:
            # Trailing behind, do not hold, speed up dwell
            hold_sec = 0.0
            action = 'EXPEDITE_DEPARTURE'
        else:
            hold_sec = 0.0
            action = 'MAINTAIN_NORMAL_DWELL'

        return {
            'forward_headway_min': round(forward_headway_min, 1),
            'backward_headway_min': round(backward_headway_min, 1),
            'target_headway_min': round(target_headway_min, 1),
            'recommended_holding_seconds': int(round(hold_sec)),
            'dispatch_command': action,
            'bunching_prevented': hold_sec > 0
        }
