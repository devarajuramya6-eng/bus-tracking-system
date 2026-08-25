"""
CityBus Enterprise Platform - On-Time Performance (OTP) Service Engine
File: backend/services/network_performance/otp_service_metrics.py

Calculates transit On-Time Performance (OTP) compliance per standard industry definitions:
- EARLY: Arrives > 1 minute before scheduled time (Early departures violate service contracts)
- ON_TIME: Between -1.0 min early and +5.0 min late
- LATE: Arrives > 5.0 min and <= 15.0 min late
- SEVERELY_LATE: Arrives > 15.0 min late
"""

from typing import List, Dict, Any


class OnTimePerformanceEngine:
    @staticmethod
    def calculate_route_otp(trip_arrivals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes aggregate OTP metrics across scheduled trips.
        """
        if not trip_arrivals:
            return {'total_trips': 0, 'otp_percentage': 0.0}

        total = len(trip_arrivals)
        early_count = 0
        ontime_count = 0
        late_count = 0
        severely_late_count = 0

        for t in trip_arrivals:
            delay_min = t.get('delay_minutes', 0.0)
            if delay_min < -1.0:
                early_count += 1
            elif delay_min <= 5.0:
                ontime_count += 1
            elif delay_min <= 15.0:
                late_count += 1
            else:
                severely_late_count += 1

        otp_pct = (ontime_count / total) * 100.0

        return {
            'total_trips_evaluated': total,
            'on_time_trips': ontime_count,
            'early_trips': early_count,
            'late_trips': late_count,
            'severely_late_trips': severely_late_count,
            'otp_compliance_percentage': round(otp_pct, 1),
            'service_grade': 'EXCELLENT' if otp_pct >= 90.0 else ('SATISFACTORY' if otp_pct >= 80.0 else 'NEEDS_INTERVENTION')
        }
