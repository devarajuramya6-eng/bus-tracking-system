"""
CityBus Enterprise Platform - Stop Service
File: backend/services/stop_service.py

Handles transit stop discovery, Haversine geospatial proximity searches,
stop shelter asset inventory, wheelchair accessibility tags, and arrival timetables.
"""

from typing import Dict, List, Any, Optional, Tuple
from repositories.stop_repository import StopRepository
from repositories.audit_repository import AuditRepository
from models import Stop, RouteStop, Route, Bus, db


class StopService:
    """Business logic for municipal bus stops and stations."""

    @staticmethod
    def get_stops_catalog(search: Optional[str] = None, wheelchair_only: bool = False,
                           popular_only: bool = False, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """Returns paginated catalog of stops with serving route tallies."""
        stops, total = StopRepository.get_all(search=search, wheelchair_only=wheelchair_only,
                                              popular_only=popular_only, page=page, per_page=per_page)
        
        stop_list = []
        for s in stops:
            s_dict = s.to_dict()
            serving_routes = StopRepository.get_routes_for_stop(s.id)
            s_dict['serving_routes_count'] = len(serving_routes)
            s_dict['serving_routes'] = serving_routes
            stop_list.append(s_dict)

        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "stops": stop_list
        }

    @staticmethod
    def get_stop_details(stop_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Fetches single stop details with full serving route list."""
        stop = StopRepository.get_by_id(stop_id)
        if not stop:
            return None, f"Stop with ID {stop_id} not found"

        stop_dict = stop.to_dict()
        routes = StopRepository.get_routes_for_stop(stop_id)
        stop_dict['serving_routes'] = routes
        return stop_dict, None

    @staticmethod
    def find_nearby_stops(user_lat: float, user_lng: float, radius_km: float = 5.0, limit: int = 20) -> List[Dict[str, Any]]:
        """Finds closest transit stops and enriches each stop with approaching bus count."""
        nearby = StopRepository.get_nearby(user_lat, user_lng, radius_km=radius_km, limit=limit)
        for s in nearby:
            s_id = s.get('id')
            if s_id:
                s['serving_routes'] = StopRepository.get_routes_for_stop(s_id)
        return nearby

    @staticmethod
    def create_stop(name: str, latitude: float, longitude: float, stop_code: Optional[str] = None,
                    landmark: Optional[str] = None, has_shelter: bool = True,
                    is_wheelchair_accessible: bool = True, is_popular: bool = False) -> Dict[str, Any]:
        """Creates a new stop record."""
        stop = StopRepository.create(
            name=name,
            latitude=latitude,
            longitude=longitude,
            stop_code=stop_code,
            landmark=landmark,
            has_shelter=has_shelter,
            is_wheelchair_accessible=is_wheelchair_accessible,
            is_popular=is_popular
        )
        AuditRepository.log_event("STOP_CREATED", "Stop", stop.id, None, None, f"Name: {stop.name}")
        return stop.to_dict()

    @staticmethod
    def update_stop(stop_id: int, **kwargs) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Updates stop attributes."""
        stop = StopRepository.update(stop_id, **kwargs)
        if not stop:
            return None, "Stop not found"
        AuditRepository.log_event("STOP_UPDATED", "Stop", stop_id, None, None)
        return stop.to_dict(), None

    @staticmethod
    def delete_stop(stop_id: int) -> Tuple[bool, Optional[str]]:
        """Deletes a stop if unreferenced."""
        success, err = StopRepository.delete(stop_id)
        if success:
            AuditRepository.log_event("STOP_DELETED", "Stop", stop_id, None, None)
        return success, err
