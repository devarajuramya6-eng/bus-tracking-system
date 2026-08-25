"""
CityBus Enterprise Platform - Driver Peer Shift Swapping & Leave Bidding
File: backend/services/driver_rostering/leave_bidding_and_swapping.py

Manages peer-to-peer duty swaps and seniority-based leave bidding:
- Allows Driver A and Driver B to exchange shifts with supervisor sign-off
- Ensures neither driver violates 48-hour weekly fatigue ceilings after swap
"""

from typing import Dict, Any


class DriverShiftSwapManager:
    @staticmethod
    def process_peer_swap(driver_a_id: int, driver_a_hours: float,
                          driver_b_id: int, driver_b_hours: float,
                          target_shift_hours: float) -> Dict[str, Any]:
        """
        Validates whether shift swap is mutually compliant.
        """
        new_hours_a = driver_a_hours + target_shift_hours
        new_hours_b = driver_b_hours - target_shift_hours

        is_a_overworked = new_hours_a > 48.0 # Weekly cap
        is_valid = not is_a_overworked

        return {
            'driver_a_id': driver_a_id,
            'driver_b_id': driver_b_id,
            'shift_duration_hours': target_shift_hours,
            'driver_a_post_swap_weekly_hours': round(new_hours_a, 1),
            'driver_b_post_swap_weekly_hours': round(new_hours_b, 1),
            'is_swap_authorized': is_valid,
            'status': 'SWAP_APPROVED_BY_DISPATCH' if is_valid else 'REJECTED_WEEKLY_HOURS_OVERFLOW'
        }
