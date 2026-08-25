"""
CityBus Enterprise Platform - Trip Repository
File: backend/repositories/trip_repository.py
"""

from datetime import datetime
from models import db, Trip, Bus, Driver


class TripRepository:
    """Isolates database operations for Trip lifecycles."""

    @staticmethod
    def get_all(status=None, driver_id=None, limit=50):
        query = Trip.query
        if status:
            query = query.filter_by(status=status)
        if driver_id:
            query = query.filter_by(driver_id=driver_id)
        return query.order_by(Trip.start_time.desc()).limit(limit).all()

    @staticmethod
    def get_by_id(trip_id):
        return Trip.query.get(trip_id)

    @staticmethod
    def get_active_trip_for_bus(bus_id):
        return Trip.query.filter_by(bus_id=bus_id, status='Active').order_by(Trip.id.desc()).first()

    @staticmethod
    def start_trip(bus_id, driver_id, route_id, conductor_id=None):
        new_trip = Trip(
            bus_id=bus_id,
            driver_id=driver_id,
            route_id=route_id,
            conductor_id=conductor_id,
            start_time=datetime.utcnow(),
            status="Active"
        )
        db.session.add(new_trip)

        # Update Bus status & assignments
        bus = Bus.query.get(bus_id)
        if bus:
            bus.status = "On Route"
            bus.driver_id = driver_id
            bus.route_id = route_id
            bus.conductor_id = conductor_id
            bus.last_gps_update = datetime.utcnow()

        # Update Driver status
        driver = Driver.query.get(driver_id)
        if driver:
            driver.status = "Active"

        db.session.commit()
        return new_trip

    @staticmethod
    def stop_trip(trip_id=None, bus_id=None):
        trip = None
        if trip_id:
            trip = Trip.query.get(trip_id)
        elif bus_id:
            trip = Trip.query.filter_by(bus_id=bus_id, status="Active").order_by(Trip.id.desc()).first()

        if trip:
            trip.end_time = datetime.utcnow()
            trip.status = "Completed"

            bus = Bus.query.get(trip.bus_id)
            if bus:
                bus.status = "Offline"
                bus.speed = 0.0
                bus.last_gps_update = datetime.utcnow()

            db.session.commit()
            return trip
        return None
