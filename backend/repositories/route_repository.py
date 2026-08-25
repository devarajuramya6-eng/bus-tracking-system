"""
CityBus Enterprise Platform - Route & Stop Repository
File: backend/repositories/route_repository.py
"""

from models import db, Route, Stop, RouteStop, Schedule


class RouteRepository:
    """Isolates all database queries related to Routes, Stops, and RouteStops."""

    @staticmethod
    def get_all(category=None):
        query = Route.query
        if category and category != 'All Routes':
            query = query.filter_by(category=category)
        return query.all()

    @staticmethod
    def get_by_id(route_id):
        return Route.query.get(route_id)

    @staticmethod
    def get_by_number(route_number):
        return Route.query.filter_by(route_number=route_number).first()

    @staticmethod
    def get_all_stops(route_id=None):
        if route_id:
            return Stop.query.join(RouteStop).filter(RouteStop.route_id == route_id).order_by(RouteStop.stop_order).all()
        return Stop.query.all()

    @staticmethod
    def get_stop_by_id(stop_id):
        return Stop.query.get(stop_id)

    @staticmethod
    def get_stop_by_code(code):
        return Stop.query.filter_by(code=code).first()

    @staticmethod
    def get_schedules_for_route(route_id):
        return Schedule.query.filter_by(route_id=route_id, is_active=True).all()
