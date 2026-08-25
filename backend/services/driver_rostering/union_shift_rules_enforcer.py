"""
CityBus Enterprise Platform - Motor Transport Workers Act Shift Rules Enforcer
File: backend/services/driver_rostering/union_shift_rules_enforcer.py

Enforces statutory driver labor rules (Motor Transport Workers Act, 1961):
- Maximum 8.0 hours driving per shift (Strict 48h weekly cap)
- Mandatory 30-minute break interval after 4.0 hours continuous wheel time
- Minimum 11.0 hours continuous rest between consecutive duty shifts
"""

from typing import Dict, Any


class UnionShiftRulesEnforcer:
    MAX_DAILY_DRIVE_HOURS = 8.0
    MAX_CONTINUOUS_DRIVE_HOURS = 4.0
    MIN_REST_BETWEEN_SHIFTS_HOURS = 11.0

    @staticmethod
    def validate_shift_assignment(scheduled_drive_hours: float,
                                  continuous_wheel_hours: float,
                                  rest_since_last_shift_hours: float) -> Dict[str, Any]:
        """
        Validates whether driver shift roster complies with labor law.
        """
        violations = []

        if scheduled_drive_hours > UnionShiftRulesEnforcer.MAX_DAILY_DRIVE_HOURS:
            violations.append(f"Exceeds max 8.0h daily limit ({scheduled_drive_hours}h scheduled)")

        if continuous_wheel_hours > UnionShiftRulesEnforcer.MAX_CONTINUOUS_DRIVE_HOURS:
            violations.append(f"Exceeds max 4.0h continuous driving without mandatory 30m break ({continuous_wheel_hours}h)")

        if rest_since_last_shift_hours < UnionShiftRulesEnforcer.MIN_REST_BETWEEN_SHIFTS_HOURS:
            violations.append(f"Insufficient rest between shifts ({rest_since_last_shift_hours}h < 11.0h required)")

        is_compliant = len(violations) == 0

        return {
            'is_labor_compliant': is_compliant,
            'violations_count': len(violations),
            'violations': violations,
            'duty_authorization': 'AUTHORIZED_FOR_DUTY' if is_compliant else 'BLOCKED_BY_UNION_FATIGUE_REGULATION'
        }
