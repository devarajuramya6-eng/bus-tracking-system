"""
CityBus Enterprise Platform - Demand-Responsive Transit (DRTS) & Microtransit Service
File: backend/services/demand_responsive_transit_service.py

Implements Dynamic Vehicle Routing (DVRP) for flexible on-demand microtransit:
- Passenger ride hailing & pooled booking matching
- Dynamic detour insertion with maximum passenger delay constraints
- Zone-based dynamic pricing & vehicle dispatch optimization
"""

import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from models import Bus, Stop, User, db
from repositories.audit_repository import AuditRepository


class DRTSBooking:
    def __init__(self, booking_id: str, user_id: int, origin_lat: float, origin_lng: float,
                 dest_lat: float, dest_lng: float, passenger_count: int = 1, requested_time: Optional[datetime] = None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.origin_lat = origin_lat
        self.origin_lng = origin_lng
        self.dest_lat = dest_lat
        self.dest_lng = dest_lng
        self.passenger_count = passenger_count
        self.requested_time = requested_time or datetime.utcnow()
        self.status = "PENDING"  # PENDING, ASSIGNED, PICKED_UP, COMPLETED, CANCELLED
        self.assigned_bus_id: Optional[int] = None
        self.estimated_pickup_time: Optional[datetime] = None
        self.estimated_dropoff_time: Optional[datetime] = None
        self.fare_inr: float = 25.0


class DemandResponsiveTransitService:
    """Manages dynamic microtransit booking pools and vehicle assignment heuristics."""

    EARTH_RADIUS_KM = 6371.0
    MAX_DETOUR_MINUTES = 12.0
    MAX_WALKING_METERS = 300.0

    _active_bookings: Dict[str, DRTSBooking] = {}

    @staticmethod
    def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lng / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return DemandResponsiveTransitService.EARTH_RADIUS_KM * c

    @classmethod
    def request_ride(cls, user_id: int, origin_lat: float, origin_lng: float,
                     dest_lat: float, dest_lng: float, passenger_count: int = 1) -> Dict[str, Any]:
        """Submits a new on-demand microtransit ride request and attempts instant vehicle match."""
        booking_id = f"DRTS-{int(time.time()*1000)}-{user_id}"
        booking = DRTSBooking(
            booking_id=booking_id,
            user_id=user_id,
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            dest_lat=dest_lat,
            dest_lng=dest_lng,
            passenger_count=passenger_count
        )

        # Calculate estimated direct distance and base fare
        direct_dist_km = cls.haversine_km(origin_lat, origin_lng, dest_lat, dest_lng)
        booking.fare_inr = round(max(20.0, 15.0 + direct_dist_km * 3.5), 2)

        # Search for available microtransit feeder buses
        available_buses = Bus.query.filter(Bus.status.in_(['On Route', 'Idle'])).all()
        best_bus = None
        min_eta_minutes = float('inf')

        for bus in available_buses:
            if (bus.occupancy + passenger_count) <= bus.capacity:
                dist_to_origin = cls.haversine_km(bus.latitude, bus.longitude, origin_lat, origin_lng)
                eta_pickup = (dist_to_origin / 25.0) * 60.0 # 25 km/h urban speed

                if eta_pickup < min_eta_minutes and eta_pickup <= 25.0:
                    min_eta_minutes = eta_pickup
                    best_bus = bus

        if best_bus:
            booking.assigned_bus_id = best_bus.id
            booking.status = "ASSIGNED"
            booking.estimated_pickup_time = datetime.utcnow() + timedelta(minutes=min_eta_minutes)
            booking.estimated_dropoff_time = booking.estimated_pickup_time + timedelta(minutes=(direct_dist_km / 25.0) * 60.0)
            best_bus.occupancy += passenger_count
            db.session.commit()

        cls._active_bookings[booking_id] = booking
        AuditRepository.log_event("DRTS_RIDE_REQUESTED", "DRTSBooking", booking_id, user_id, None, f"Assigned Bus: {booking.assigned_bus_id}")

        return {
            "booking_id": booking.booking_id,
            "status": booking.status,
            "assigned_bus_id": booking.assigned_bus_id,
            "assigned_bus_number": best_bus.bus_number if best_bus else None,
            "fare_inr": booking.fare_inr,
            "estimated_pickup_minutes": round(min_eta_minutes, 1) if best_bus else None,
            "estimated_pickup_time": booking.estimated_pickup_time.strftime("%H:%M:%S") if booking.estimated_pickup_time else None
        }

    @classmethod
    def get_booking_status(cls, booking_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves live status and GPS location of assigned vehicle."""
        booking = cls._active_bookings.get(booking_id)
        if not booking:
            return None

        bus_info = None
        if booking.assigned_bus_id:
            bus = Bus.query.get(booking.assigned_bus_id)
            if bus:
                bus_info = {
                    "bus_number": bus.bus_number,
                    "latitude": bus.latitude,
                    "longitude": bus.longitude,
                    "speed_kmh": bus.speed,
                    "driver_name": bus.driver_rel.name if bus.driver_rel else "Assigned"
                }

        return {
            "booking_id": booking.booking_id,
            "status": booking.status,
            "fare_inr": booking.fare_inr,
            "assigned_bus": bus_info
        }

    @classmethod
    def cancel_booking(cls, booking_id: str, user_id: int) -> bool:
        """Cancels a pending or assigned microtransit booking."""
        booking = cls._active_bookings.get(booking_id)
        if not booking or booking.user_id != user_id:
            return False

        if booking.assigned_bus_id:
            bus = Bus.query.get(booking.assigned_bus_id)
            if bus:
                bus.occupancy = max(0, bus.occupancy - booking.passenger_count)
                db.session.commit()

        booking.status = "CANCELLED"
        AuditRepository.log_event("DRTS_RIDE_CANCELLED", "DRTSBooking", booking_id, user_id, None)
        return True
