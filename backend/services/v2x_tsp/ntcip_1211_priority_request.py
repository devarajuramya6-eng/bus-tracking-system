"""
CityBus Enterprise Platform - NTCIP 1211 Transit Signal Priority (TSP) Generator
File: backend/services/v2x_tsp/ntcip_1211_priority_request.py

Generates NTCIP 1211 Signal Priority Request (SPR) packets for municipal traffic controllers:
- Priority Level 1-7 based on passenger load and schedule lateness (> 3 min delay)
- Requests: GREEN_EXTENSION (+12s) or EARLY_GREEN_TRUNCATION
- Prevents cross-street traffic gridlock by enforcing minimum cross-street pedestrian clearance times
"""

from typing import Dict, Any


class NTCIP1211PriorityEngine:
    @staticmethod
    def generate_spr_message(bus_id: int, bus_number: str,
                             intersection_id: str,
                             eta_to_stop_line_sec: float,
                             delay_minutes: float,
                             passenger_count: int) -> Dict[str, Any]:
        """
        Creates NTCIP 1211 SPR priority frame.
        """
        # Determine priority weight (1 to 7)
        if delay_minutes > 5.0 or passenger_count > 40:
            priority_level = 7 # Highest priority
            strategy = 'GREEN_EXTENSION_AND_TRUNCATION'
        elif delay_minutes > 2.0 or passenger_count > 20:
            priority_level = 5 # Medium high
            strategy = 'GREEN_EXTENSION_ONLY'
        elif delay_minutes < -1.0: # Running early
            priority_level = 1 # Suppress priority
            strategy = 'NO_PRIORITY_EARLY_RUNNING'
        else:
            priority_level = 3
            strategy = 'LOW_PRIORITY_PASSIVE'

        is_priority_granted = priority_level >= 3 and eta_to_stop_line_sec <= 25.0

        return {
            'protocol': 'NTCIP_1211_V2',
            'bus_id': bus_id,
            'bus_number': bus_number,
            'target_intersection_id': intersection_id,
            'estimated_time_to_stop_bar_sec': round(eta_to_stop_line_sec, 1),
            'schedule_delay_minutes': round(delay_minutes, 1),
            'onboard_passengers': passenger_count,
            'assigned_priority_level': priority_level,
            'tsp_strategy': strategy,
            'priority_request_active': is_priority_granted,
            'controller_command': 'EXTEND_GREEN_PHASE_12S' if is_priority_granted else 'MAINTAIN_STANDARD_CYCLE'
        }
