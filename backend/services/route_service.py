"""
CityBus Enterprise Platform - Route & Transit Corridor Service
File: backend/services/route_service.py

Provides transit corridor analytics, stop sequence management, route geometry
polyline generation, distance/duration matrix calculation, and GTFS export helpers.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from repositories.route_repository import RouteRepository
from repositories.stop_repository import StopRepository
from repositories.audit_repository import AuditRepository
from models import Route, Stop, RouteStop, Bus, db


class RouteService:
    """Business logic for transit routes and corridor geometry."""

    @staticmethod
    def get_route_catalog(category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns catalog of all active routes with stop count and live bus tally."""
        routes = RouteRepository.get_all(category=category, search=search)
        catalog = []
        for r in routes:
            r_dict = r.to_dict(include_stops=False)
            buses_count = Bus.query.filter_by(route_id=r.id, status='On Route').count()
            r_dict['live_buses_count'] = buses_count
            catalog.append(r_dict)
        return catalog

    @staticmethod
    def get_route_details(route_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Returns route details including full sequenced stops and polyline waypoints."""
        route = RouteRepository.get_by_id(route_id)
        if not route:
            return None, f"Route with ID {route_id} not found"

        route_dict = route.to_dict(include_stops=True)
        # Fetch active buses operating on this corridor
        active_buses = Bus.query.filter_by(route_id=route_id).all()
        route_dict['active_buses'] = [b.to_dict() for b in active_buses]
        route_dict['waypoints'] = route.get_waypoints()
        return route_dict, None

    @staticmethod
    def create_route(route_number: str, name: str, start_point: str, destination: str,
                     category: str = "Local", estimated_time: int = 30, distance_km: float = 12.0,
                     base_fare: float = 15.0, color_hex: str = "#2563EB",
                     waypoints: Optional[List[List[float]]] = None, stop_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        """Creates a new transit corridor with waypoints and ordered stop links."""
        route = Route(
            route_number=route_number.strip().upper(),
            name=name.strip(),
            start_point=start_point.strip(),
            destination=destination.strip(),
            category=category.strip(),
            estimated_time=estimated_time,
            distance_km=distance_km,
            base_fare=base_fare,
            color_hex=color_hex.strip(),
            waypoints_json=json.dumps(waypoints or []),
            status="Active"
        )
        db.session.add(route)
        db.session.flush()

        # Link stops in sequence if provided
        if stop_ids:
            for idx, stop_id in enumerate(stop_ids, start=1):
                rs = RouteStop(
                    route_id=route.id,
                    stop_id=stop_id,
                    stop_order=idx,
                    duration_from_origin_min=int((idx - 1) * (estimated_time / max(1, len(stop_ids) - 1))),
                    fare_from_origin=round(base_fare * (idx / len(stop_ids)), 1)
                )
                db.session.add(rs)

        db.session.commit()
        AuditRepository.log_event("ROUTE_CREATED", "Route", route.id, None, None, f"Route: {route.route_number}")

        return route.to_dict(include_stops=True)

    @staticmethod
    def update_route_stops(route_id: int, stop_ids: List[int]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Re-sequences and links stops to a route."""
        route = RouteRepository.get_by_id(route_id)
        if not route:
            return None, "Route not found"

        # Delete existing sequence
        RouteStop.query.filter_by(route_id=route_id).delete()

        # Insert new sequence
        for idx, s_id in enumerate(stop_ids, start=1):
            rs = RouteStop(
                route_id=route.id,
                stop_id=s_id,
                stop_order=idx,
                duration_from_origin_min=int((idx - 1) * (route.estimated_time / max(1, len(stop_ids) - 1))),
                fare_from_origin=round(route.base_fare * (idx / len(stop_ids)), 1)
            )
            db.session.add(rs)

        db.session.commit()
        AuditRepository.log_event("ROUTE_STOPS_UPDATED", "Route", route_id, None, None)

        return route.to_dict(include_stops=True), None

    @staticmethod
    def get_corridor_statistics(route_id: int) -> Dict[str, Any]:
        """Calculates corridor performance KPIs: average speeds, on-time headway, and load factor."""
        route = RouteRepository.get_by_id(route_id)
        if not route:
            return {}

        buses = Bus.query.filter_by(route_id=route_id).all()
        total_capacity = sum(b.capacity for b in buses)
        total_passengers = sum(b.occupancy for b in buses)
        load_factor = round((total_passengers / max(1, total_capacity)) * 100.0, 1)

        return {
            "route_id": route.id,
            "route_number": route.route_number,
            "distance_km": route.distance_km,
            "estimated_time_min": route.estimated_time,
            "operating_buses_count": len(buses),
            "total_corridor_capacity": total_capacity,
            "current_passengers_on_route": total_passengers,
            "corridor_load_factor_pct": load_factor,
            "average_bus_speed_kmh": round(sum(b.speed for b in buses) / max(1, len(buses)), 1)
        }
