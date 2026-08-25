"""
CityBus Enterprise Platform - Headway Regulation & Bus Bunching Prevention Service
File: backend/services/headway_service.py

Monitors spatial spacing between consecutive buses on transit corridors:
- Calculates actual headway (time gap between vehicles)
- Detects Bus Bunching conditions (two buses < 2.5 minutes apart)
- Emits regulation advisories (e.g. "Hold bus 90 seconds at next stop" or "Skip minor stop")
"""

import math
from models import db, Bus, Route
from repositories.bus_repository import BusRepository


class HeadwayService:
    @staticmethod
    def analyze_corridor_headway(route_id):
        """Analyzes spatial and temporal spacing for all active buses on a route."""
        buses = Bus.query.filter_by(status="On Route").all()
        if len(buses) < 2:
            return {'status': 'OPTIMAL', 'active_buses': len(buses), 'alerts': []}

        alerts = []
        # Sort buses by latitude as simple progression proxy
        sorted_buses = sorted(buses, key=lambda b: (b.latitude, b.longitude))

        for i in range(len(sorted_buses) - 1):
            b1 = sorted_buses[i]
            b2 = sorted_buses[i+1]

            dist_km = BusRepository.haversine_km(b1.latitude, b1.longitude, b2.latitude, b2.longitude)
            # Estimate headway in minutes assuming 25 km/h
            estimated_headway_min = (dist_km / 25.0) * 60.0

            if estimated_headway_min < 3.0:
                alerts.append({
                    'type': 'BUS_BUNCHING_DETECTED',
                    'severity': 'High',
                    'lead_bus': b2.bus_number,
                    'trail_bus': b1.bus_number,
                    'distance_km': round(dist_km, 2),
                    'headway_minutes': round(estimated_headway_min, 1),
                    'advisory': f"Hold trailing bus {b1.bus_number} for 90 seconds at upcoming stop to restore scheduled 10-minute headway."
                })

        return {
            'route_id': route_id,
            'active_buses': len(buses),
            'bunching_count': len(alerts),
            'alerts': alerts
        }
