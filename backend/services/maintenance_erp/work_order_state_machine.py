"""
CityBus Enterprise Platform - Maintenance Work Order Finite State Machine (FSM)
File: backend/services/maintenance_erp/work_order_state_machine.py

Controls workshop job card lifecycle transitions:
- DRAFT ➔ APPROVED ➔ IN_PROGRESS ➔ AWAITING_PARTS ➔ QC_INSPECTED ➔ CLOSED
- Enforces mandatory Quality Control (QC) supervisor sign-off before releasing bus to dispatch
"""

from typing import Dict, Any, Set


class WorkOrderStateMachine:
    VALID_TRANSITIONS: Dict[str, Set[str]] = {
        'DRAFT': {'APPROVED', 'CANCELLED'},
        'APPROVED': {'IN_PROGRESS', 'AWAITING_PARTS', 'CANCELLED'},
        'IN_PROGRESS': {'AWAITING_PARTS', 'QC_INSPECTION_PENDING'},
        'AWAITING_PARTS': {'IN_PROGRESS', 'CANCELLED'},
        'QC_INSPECTION_PENDING': {'CLOSED', 'IN_PROGRESS'}, # Can fail QC and return to progress
        'CLOSED': set(),
        'CANCELLED': set()
    }

    @staticmethod
    def transition_state(current_state: str, next_state: str, supervisor_id: int = None) -> Dict[str, Any]:
        """
        Validates and applies job card status transition.
        """
        curr = current_state.upper().strip()
        nxt = next_state.upper().strip()

        allowed = WorkOrderStateMachine.VALID_TRANSITIONS.get(curr, set())

        if nxt not in allowed:
            return {
                'success': False,
                'current_state': curr,
                'attempted_state': nxt,
                'error': f"Illegal transition from {curr} to {nxt}."
            }

        # QC inspection requires supervisor sign-off
        if nxt == 'CLOSED' and not supervisor_id:
            return {
                'success': False,
                'error': 'QC sign-off requires valid supervisor_id.'
            }

        return {
            'success': True,
            'previous_state': curr,
            'new_state': nxt,
            'is_vehicle_roadworthy': nxt == 'CLOSED',
            'status': 'TRANSITION_SUCCESS'
        }
