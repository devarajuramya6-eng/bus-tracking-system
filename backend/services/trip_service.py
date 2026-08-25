"""
CityBus Enterprise Platform - Trip Operations Service
File: backend/services/trip_service.py
"""

from repositories.trip_repository import TripRepository
from repositories.user_repository import UserRepository


class TripService:
    """Manages driver trip lifecycles, stop progress, and passenger count logging."""

    @staticmethod
    def start_trip(bus_id, driver_id, route_id, conductor_id=None):
        trip = TripRepository.start_trip(bus_id, driver_id, route_id, conductor_id)
        UserRepository.log_audit("TRIP_START", "Trip", trip.id, f"Trip {trip.id} started for Bus {bus_id} by Driver {driver_id}")
        return trip

    @staticmethod
    def stop_trip(trip_id=None, bus_id=None):
        trip = TripRepository.stop_trip(trip_id, bus_id)
        if trip:
            UserRepository.log_audit("TRIP_STOP", "Trip", trip.id, f"Trip {trip.id} ended")
        return trip

    @staticmethod
    def update_passenger_occupancy(trip_id, count_delta):
        trip = TripRepository.get_by_id(trip_id)
        if trip:
            trip.passenger_boarded_count = max(0, trip.passenger_boarded_count + count_delta)
            
            from models import Bus
            bus = Bus.query.get(trip.bus_id)
            if bus:
                bus.occupancy = trip.passenger_boarded_count
                bus.save()
            trip.save()
            return trip
        return None
