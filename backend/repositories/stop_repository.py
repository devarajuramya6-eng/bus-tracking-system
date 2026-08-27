"""
CityBus Enterprise Platform - Stop Repository
File: backend/repositories/stop_repository.py

Encapsulates data access and geospatial proximity search for Transit Stops,
shelters, wheelchair accessibility flags, and route stop associations.
"""

import math
from models import db, Stop, RouteStop, Route
from sqlalchemy import or_


class StopRepository:
    """Data access layer for municipal bus stops and stations."""

    @staticmethod
    def get_all(search=None, wheelchair_only=False, popular_only=False, page=1, per_page=50):
        """Retrieves stops with filtering, search, and pagination."""
        query = Stop.query
        if wheelchair_only:
            query = query.filter_by(is_wheelchair_accessible=True)
        if popular_only:
            query = query.filter_by(is_popular=True)
        if search:
            s = f"%{search}%"
            query = query.filter(or_(
                Stop.name.ilike(s),
                Stop.stop_code.ilike(s),
                Stop.landmark.ilike(s)
            ))
            
        total = query.count()
        stops = query.order_by(Stop.name.asc()).offset((page - 1) * per_page).limit(per_page).all()
        return stops, total

    @staticmethod
    def get_by_id(stop_id):
        """Fetches stop by ID."""
        return Stop.query.get(stop_id)

    @staticmethod
    def get_by_code(stop_code):
        """Fetches stop by unique stop_code (e.g., STP-001)."""
        return Stop.query.filter_by(stop_code=stop_code.strip().upper()).first()

    @staticmethod
    def create(name, latitude, longitude, stop_code=None, landmark=None, has_shelter=True, is_wheelchair_accessible=True, is_popular=False):
        """Creates a new transit stop."""
        if not stop_code:
            count = Stop.query.count()
            stop_code = f"STP-{count + 1:04d}"
            
        stop = Stop(
            name=name.strip(),
            stop_code=stop_code.strip().upper(),
            latitude=float(latitude),
            longitude=float(longitude),
            landmark=landmark.strip() if landmark else None,
            has_shelter=has_shelter,
            is_wheelchair_accessible=is_wheelchair_accessible,
            is_popular=is_popular
        )
        db.session.add(stop)
        db.session.commit()
        return stop

    @staticmethod
    def update(stop_id, **kwargs):
        """Updates stop attributes."""
        stop = Stop.query.get(stop_id)
        if not stop:
            return None
        for key, val in kwargs.items():
            if hasattr(stop, key) and key != 'id':
                setattr(stop, key, val)
        db.session.commit()
        return stop

    @staticmethod
    def delete(stop_id):
        """Deletes a stop if not referenced by active routes."""
        stop = Stop.query.get(stop_id)
        if not stop:
            return False, "Stop not found"
            
        route_stops = RouteStop.query.filter_by(stop_id=stop_id).count()
        if route_stops > 0:
            return False, f"Stop is referenced by {route_stops} route sequence(s)"
            
        db.session.delete(stop)
        db.session.commit()
        return True, None

    @staticmethod
    def get_nearby(user_lat, user_lng, radius_km=5.0, limit=20):
        """Finds closest transit stops using Haversine spherical distance."""
        all_stops = Stop.query.all()
        nearby = []
        
        for stop in all_stops:
            # Haversine calculation
            d_lat = math.radians(stop.latitude - user_lat)
            d_lng = math.radians(stop.longitude - user_lng)
            a = (math.sin(d_lat / 2.0) ** 2 +
                 math.cos(math.radians(user_lat)) * math.cos(math.radians(stop.latitude)) *
                 math.sin(d_lng / 2.0) ** 2)
            c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
            dist_km = 6371.0 * c
            
            if dist_km <= radius_km:
                stop_dict = stop.to_dict()
                stop_dict['distance_km'] = round(dist_km, 2)
                stop_dict['distance_meters'] = int(dist_km * 1000)
                nearby.append(stop_dict)
                
        nearby.sort(key=lambda s: s['distance_km'])
        return nearby[:limit]

    @staticmethod
    def get_routes_for_stop(stop_id):
        """Returns all routes that serve the given stop."""
        route_stops = RouteStop.query.filter_by(stop_id=stop_id).order_by(RouteStop.stop_order.asc()).all()
        routes = []
        seen = set()
        for rs in route_stops:
            if rs.route_id not in seen:
                seen.add(rs.route_id)
                route = Route.query.get(rs.route_id)
                if route:
                    routes.append({
                        "route_id": route.id,
                        "route_number": route.route_number,
                        "name": route.name,
                        "stop_order": rs.stop_order,
                        "fare_from_origin": rs.fare_from_origin,
                        "duration_from_origin_min": rs.duration_from_origin_min
                    })
        return routes
