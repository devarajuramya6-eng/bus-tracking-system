"""
CityBus Enterprise Platform - Incident Management Workflow Engine
File: backend/services/incident_workflow_engine.py

Governs the finite state machine transitions for emergency SOS and road accidents:
NEW -> ACKNOWLEDGED -> DISPATCHED -> ON_SCENE -> RESOLVED -> CLOSED.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from models import Incident, Bus, db
from repositories.audit_repository import AuditRepository


class IncidentWorkflowEngine:
    """Finite State Machine for municipal transit incidents and SOS triage."""

    VALID_TRANSITIONS = {
        'OPEN': ['ACKNOWLEDGED', 'DISPATCHED', 'RESOLVED', 'CLOSED'],
        'ACKNOWLEDGED': ['DISPATCHED', 'ON_SCENE', 'RESOLVED', 'CLOSED'],
        'DISPATCHED': ['ON_SCENE', 'RESOLVED', 'CLOSED'],
        'ON_SCENE': ['RESOLVED', 'CLOSED'],
        'RESOLVED': ['CLOSED'],
        'CLOSED': []
    }

    @staticmethod
    def transition_state(incident_id: int, target_status: str, operator_id: Optional[int] = None, notes: str = '') -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Validates and executes state transition for an incident ticket."""
        incident = Incident.query.get(incident_id)
        if not incident:
            return None, f"Incident {incident_id} not found"

        current = (incident.status or 'OPEN').upper()
        target = target_status.upper()

        if target not in IncidentWorkflowEngine.VALID_TRANSITIONS.get(current, []):
            return None, f"Illegal state transition from {current} to {target}"

        incident.status = target
        if notes:
            incident.resolution_notes = f"{incident.resolution_notes or ''}\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] {notes}".strip()

        if target == 'RESOLVED' or target == 'CLOSED':
            incident.resolved_at = datetime.utcnow()
            # If bus was in Emergency state, restore to On Route or Offline
            bus = Bus.query.get(incident.bus_id)
            if bus and bus.status == 'Emergency':
                bus.status = 'On Route'

        db.session.commit()
        AuditRepository.log_event(f"INCIDENT_TRANSITION_{target}", "Incident", incident.id, operator_id, None, f"Notes: {notes}")

        return incident.to_dict(), None
