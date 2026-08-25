"""
CityBus Enterprise Platform - Digital Speed Governor Telematics Enforcement
File: backend/services/safety/speed_governor_enforcement.py

Enforces AIS-018 / AIS-140 statutory Speed Limiting Function (SLF):
- Commercial transit bus statutory cap: 60.0 km/h (80.0 km/h on expressways)
- Governor wire disconnection / tamper detection
- Automated transport department compliance violation logs
"""

from datetime import datetime
from typing import Dict, Any, List


class SpeedGovernorEnforcement:
    MUNICIPAL_SPEED_CAP_KMH = 60.0

    @staticmethod
    def audit_speed_governor(bus_id: int, bus_number: str,
                             current_speed_kmh: float,
                             governor_pulse_active: bool,
                             throttle_pct: float) -> Dict[str, Any]:
        """
        Audits physical speed governor compliance and detects tampering.
        """
        is_tampered = not governor_pulse_active and current_speed_kmh > 10.0
        is_overspeeding = current_speed_kmh > (SpeedGovernorEnforcement.MUNICIPAL_SPEED_CAP_KMH + 3.0)

        alert_type = 'COMPLIANT'
        severity = 'NONE'

        if is_tampered:
            alert_type = 'SPEED_GOVERNOR_TAMPER_DETECTED'
            severity = 'CRITICAL'
        elif is_overspeeding:
            alert_type = 'AIS140_STATUTORY_OVERSPEED'
            severity = 'HIGH'

        return {
            'bus_id': bus_id,
            'bus_number': bus_number,
            'current_speed_kmh': round(current_speed_kmh, 1),
            'statutory_limit_kmh': SpeedGovernorEnforcement.MUNICIPAL_SPEED_CAP_KMH,
            'throttle_position_pct': throttle_pct,
            'governor_active': governor_pulse_active,
            'is_tampered': is_tampered,
            'is_overspeeding': is_overspeeding,
            'alert_type': alert_type,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat()
        }
