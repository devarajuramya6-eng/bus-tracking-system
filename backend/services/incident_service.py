"""
CityBus Enterprise Platform - Incident & Emergency Response Service
File: backend/services/incident_service.py
"""

from repositories.incident_repository import IncidentRepository
from repositories.user_repository import UserRepository


class IncidentService:
    """Manages incident lifecycle, Kanban transitions, and emergency panic button SOS broadcasts."""

    @staticmethod
    def report_incident(incident_type, title, description, severity="Medium", bus_id=None, driver_id=None, route_id=None, lat=None, lng=None, reported_by=None):
        inc = IncidentRepository.create_incident(
            incident_type=incident_type,
            title=title,
            description=description,
            severity=severity,
            bus_id=bus_id,
            driver_id=driver_id,
            route_id=route_id,
            lat=lat,
            lng=lng,
            reported_by=reported_by
        )
        UserRepository.log_audit("INCIDENT_REPORTED", "Incident", inc.id, f"Incident {inc.incident_number} ({severity}) reported")
        return inc

    @staticmethod
    def trigger_emergency_sos(bus_id, driver_id, lat, lng, details="Driver pressed emergency SOS panic button"):
        """High-priority emergency SOS trigger."""
        inc = IncidentRepository.create_incident(
            incident_type="SOS_Emergency",
            title=f"🚨 PRIORITY-1 EMERGENCY SOS: Bus {bus_id}",
            description=details,
            severity="Critical",
            bus_id=bus_id,
            driver_id=driver_id,
            lat=lat,
            lng=lng
        )

        from models import Bus
        bus = Bus.query.get(bus_id)
        if bus:
            bus.status = "Emergency"
            bus.save()

        UserRepository.log_audit("EMERGENCY_SOS", "Incident", inc.id, f"EMERGENCY SOS triggered on Bus {bus_id}")
        return inc
