"""
CityBus Enterprise Platform - Incident Triage & Automated Dispatch Escalation
File: backend/services/incidents_adv/incident_triage_engine.py

Classifies incoming field incidents and triggers automated SOP actions:
- Level 1 (LOW): Fare dispute, route query ➔ In-app conductor resolution
- Level 2 (MEDIUM): Flat tire, minor coolant leak ➔ Roadside Mobile Van dispatch
- Level 3 (HIGH): Passenger medical emergency, physical altercation ➔ 108 EMS & 112 Police
- Level 4 (CRITICAL): Major collision, fire, rollover ➔ Immediate multi-agency red alert
"""

from typing import Dict, Any, List


class IncidentTriageEngine:
    @staticmethod
    def triage_incident(incident_category: str, description: str, passengers_affected: int) -> Dict[str, Any]:
        """
        Classifies incident severity and assigns emergency response level.
        """
        cat = incident_category.upper().strip()

        if any(w in cat for w in ['FIRE', 'COLLISION', 'ROLLOVER', 'CRITICAL']):
            level = 4
            severity = 'CRITICAL'
            sop = 'DISPATCH_112_POLICE_AND_108_EMS_AND_FIRE_BRIGADE'
            sla_minutes = 3
        elif any(w in cat for w in ['MEDICAL', 'FIGHT', 'SECURITY', 'PANIC']):
            level = 3
            severity = 'HIGH'
            sop = 'DISPATCH_EMS_AND_TRANSIT_POLICE'
            sla_minutes = 5
        elif any(w in cat for w in ['BREAKDOWN', 'FLAT_TIRE', 'MECHANICAL', 'OVERHEAT']):
            level = 2
            severity = 'MEDIUM'
            sop = 'DISPATCH_ROADSIDE_RECOVERY_VAN_AND_STANDBY_BUS'
            sla_minutes = 15
        else:
            level = 1
            severity = 'LOW'
            sop = 'LOG_OPERATIONAL_NOTE_CONTINUE_SERVICE'
            sla_minutes = 60

        return {
            'incident_category': incident_category,
            'severity_level': level,
            'severity_name': severity,
            'sop_action_plan': sop,
            'response_sla_minutes': sla_minutes,
            'passengers_affected': passengers_affected,
            'requires_executive_escalation': level >= 3
        }
