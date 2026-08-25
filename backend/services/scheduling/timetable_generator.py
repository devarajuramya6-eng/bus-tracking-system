"""
CityBus Enterprise Platform - Clockface Timetable & Headway Generator
File: backend/services/scheduling/timetable_generator.py

Generates clockface frequency timetables with interpolated timepoint passings:
- Peak hour (8-10 min headway) vs Off-peak (15-20 min headway) service spans
- Stop-by-stop departure matrix generation
"""

from typing import List, Dict, Any


class TimetableGenerator:
    @staticmethod
    def format_time_hhmm(minutes_from_midnight: int) -> str:
        hh = (minutes_from_midnight // 60) % 24
        mm = minutes_from_midnight % 60
        return f"{hh:02d}:{mm:02d}"

    @staticmethod
    def generate_corridor_timetable(route_id: int, route_number: str,
                                    stops: List[Dict[str, Any]],
                                    first_departure_min: int = 360, # 06:00
                                    last_departure_min: int = 1380, # 23:00
                                    peak_headway_min: int = 10,
                                    offpeak_headway_min: int = 15) -> List[Dict[str, Any]]:
        """
        Builds a comprehensive tabular schedule for all daily bus departures on a route.
        """
        timetable_rows = []
        current_dep = first_departure_min
        trip_num = 1

        # Calculate standard inter-stop run times
        inter_stop_min = max(2, int(45 / max(1, len(stops) - 1)))

        while current_dep <= last_departure_min:
            is_peak = (480 <= current_dep <= 600) or (1020 <= current_dep <= 1200) # 08-10 & 17-20
            headway = peak_headway_min if is_peak else offpeak_headway_min

            stop_times = []
            accum_min = current_dep

            for s_idx, stop in enumerate(stops):
                stop_times.append({
                    'stop_id': stop.get('id', s_idx + 1),
                    'stop_name': stop.get('name', f'Stop {s_idx + 1}'),
                    'time': TimetableGenerator.format_time_hhmm(accum_min)
                })
                accum_min += inter_stop_min

            timetable_rows.append({
                'trip_number': f"TRIP-{route_number}-{trip_num:03d}",
                'departure_time': TimetableGenerator.format_time_hhmm(current_dep),
                'arrival_time': TimetableGenerator.format_time_hhmm(accum_min),
                'is_peak_trip': is_peak,
                'stop_times': stop_times
            })

            current_dep += headway
            trip_num += 1

        return timetable_rows
