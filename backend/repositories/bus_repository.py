"""
CityBus Enterprise Platform - Bus Repository
File: backend/repositories/bus_repository.py
"""

from datetime import datetime, timedelta
import math
from models import db, Bus, Telemetry


class BusRepository:
    """Isolates all database queries related to Buses and Telemetry."""

    @staticmethod
    def get_all(status=None, route_id=None, limit=100):
        query = Bus.query
        if status and status != 'All':
            query = query.filter(Bus.status.ilike(status))
        if route_id:
            query = query.filter(Bus.route_id == route_id)
        return query.limit(limit).all()

    @staticmethod
    def get_by_id(bus_id):
        return Bus.query.get(bus_id)

    @staticmethod
    def get_by_number(bus_number):
        return Bus.query.filter_by(bus_number=bus_number).first()

    @staticmethod
    def update_location(bus_id, lat, lng, speed, heading=0.0, accuracy=5.0):
        bus = Bus.query.get(bus_id)
        if not bus:
            return None

        bus.latitude = float(lat)
        bus.longitude = float(lng)
        bus.speed = float(speed)
        bus.heading = float(heading)
        bus.accuracy = float(accuracy)
        bus.last_gps_update = datetime.utcnow()

        if bus.status == 'Offline' and bus.speed > 5:
            bus.status = 'On Route'

        # Log historical telemetry ping
        telemetry = Telemetry(
            bus_id=bus.id,
            latitude=bus.latitude,
            longitude=bus.longitude,
            speed_kmh=bus.speed,
            heading_deg=bus.heading,
            accuracy_m=bus.accuracy,
            recorded_at=datetime.utcnow()
        )
        db.session.add(telemetry)
        db.session.commit()
        return bus

    @staticmethod
    def get_nearby(lat, lng, max_dist_km=15.0):
        buses = Bus.query.filter(Bus.status != 'Offline').all()
        nearby = []
        
        for b in buses:
            dist = BusRepository.haversine_km(lat, lng, b.latitude, b.longitude)
            if dist <= max_dist_km:
                bus_dict = b.to_dict()
                bus_dict['distance_km'] = round(dist, 2)
                effective_speed = b.speed if b.speed > 5 else 30.0
                bus_dict['eta_minutes'] = max(1, round((dist / effective_speed) * 60))
                nearby.append(bus_dict)

        nearby.sort(key=lambda x: x['distance_km'])
        return nearby

    @staticmethod
    def haversine_km(lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def get_stale_buses(threshold_seconds=30):
        cutoff = datetime.utcnow() - timedelta(seconds=threshold_seconds)
        return Bus.query.filter(Bus.status == 'On Route', Bus.last_gps_update < cutoff).all()
