"""
CityBus Enterprise Platform - Route Timetable & Schedule Matrix Generator
File: backend/services/route_timetable_generator.py

Generates dynamic static and frequency-based timetables across peak, off-peak,
night owl shifts, weekend schedules, and stop departure charts.
"""

from datetime import datetime, time, timedelta
from typing import Dict, List, Any, Optional
from models import Route, Stop, RouteStop, db


class RouteTimetableGenerator:
    """Generates scheduled departure matrices for public transit timetables."""

    @staticmethod
    def generate_route_timetable(route_id: int, service_day: str = "WEEKDAY") -> Dict[str, Any]:
        """Generates stop-by-stop scheduled departure times from 05:30 to 22:30."""
        route = Route.query.get(route_id)
        if not route:
            return {"error": "Route not found"}

        route_stops = RouteStop.query.filter_by(route_id=route_id).order_by(RouteStop.stop_order.asc()).all()
        stops_data = []
        for rs in route_stops:
            s = Stop.query.get(rs.stop_id)
            if s:
                stops_data.append({"stop_id": s.id, "name": s.name, "order": rs.stop_order})

        # Headway by time period: Peak (every 10m), Midday (every 15m), Night (every 20m)
        departures = []
        curr_min = 5 * 60 + 30 # 05:30 AM in minutes
        end_min = 22 * 60 + 30  # 10:30 PM

        while curr_min <= end_min:
            h = curr_min // 60
            m = curr_min % 60
            dep_time_str = f"{h:02d}:{m:02d}"

            # Calculate arrival at each stop along route
            stop_times = []
            accumulated_time = 0
            for idx, st in enumerate(stops_data):
                st_time = (curr_min + accumulated_time)
                st_h = st_time // 60
                st_m = st_time % 60
                stop_times.append({
                    "stop_name": st["name"],
                    "scheduled_time": f"{st_h:02d}:{st_m:02d}"
                })
                accumulated_time += 3 # 3 minutes between consecutive stops

            departures.append({
                "trip_code": f"TRIP-{route.route_number}-{dep_time_str.replace(':', '')}",
                "origin_departure": dep_time_str,
                "stop_times": stop_times
            })

            # Interval increment
            is_peak = (h in [8, 9, 10, 17, 18, 19])
            curr_min += (10 if is_peak else 15)

        return {
            "route_id": route.id,
            "route_number": route.route_number,
            "corridor_name": route.name,
            "service_day": service_day,
            "total_daily_trips": len(departures),
            "stops": stops_data,
            "departures": departures
        }
