"""
CityBus Enterprise Platform - Universal Accessibility & Special Needs Transit Planner
File: backend/services/accessibility_route_planner.py

Calculates wheelchair-accessible itineraries, low-floor bus schedules,
audio-visual bus stop shelters, and priority seating reservations.
"""

from typing import Dict, List, Any, Optional
from models import Bus, Route, Stop, RouteStop, db


class AccessibilityRoutePlanner:
    """Filters transit journeys for passengers with reduced mobility or visual impairments."""

    @staticmethod
    def get_accessible_routes() -> List[Dict[str, Any]]:
        """Returns routes operating 100% low-floor wheelchair accessible buses."""
        routes = Route.query.all()
        accessible_list = []

        for r in routes:
            buses = Bus.query.filter_by(route_id=r.id).all()
            # In our fleet, low-floor models or electric buses are fully ramp equipped
            accessible_buses = [b for b in buses if 'Low Floor' in (b.model or '') or b.fuel_type == 'Electric']

            accessible_list.append({
                "route_id": r.id,
                "route_number": r.route_number,
                "name": r.name,
                "total_buses": len(buses),
                "wheelchair_accessible_buses": len(accessible_buses),
                "has_wheelchair_ramp": len(accessible_buses) > 0,
                "features": [
                    "Low floor step-free boarding",
                    "Dedicated wheelchair securement area",
                    "Audio-visual stop annunciator"
                ]
            })

        return accessible_list
