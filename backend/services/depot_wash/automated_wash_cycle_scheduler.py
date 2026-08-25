"""
CityBus Enterprise Platform - Fleet Automated Wash Cycle & Sanitization Scheduler
File: backend/services/depot_wash/automated_wash_cycle_scheduler.py

Schedules automated fleet washing and interior hygiene sanitization:
- Daily Exterior Wash: Drive-through rollover brush arch upon depot return
- Weekly Interior Deep Clean: High-pressure floor wash and microbial sanitization misting
- Flags vehicles overdue for exterior or interior hygiene cycles
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


class BusWashCycleScheduler:
    @staticmethod
    def audit_bus_hygiene(bus_number: str, days_since_exterior_wash: int, days_since_interior_deep_clean: int) -> Dict[str, Any]:
        """
        Determines wash bay routing for incoming depot buses.
        """
        needs_exterior = days_since_exterior_wash >= 1
        needs_deep_clean = days_since_interior_deep_clean >= 7

        if needs_deep_clean:
            queue_bay = 'BAY_2_DEEP_CLEAN_AND_MISTING'
        elif needs_exterior:
            queue_bay = 'BAY_1_AUTOMATED_BRUSH_ROLLOVER'
        else:
            queue_bay = 'DIRECT_TO_PARKING_BERTH'

        return {
            'bus_number': bus_number,
            'days_since_exterior_wash': days_since_exterior_wash,
            'days_since_interior_clean': days_since_interior_deep_clean,
            'assigned_wash_bay': queue_bay,
            'is_hygiene_compliant': not needs_deep_clean
        }
