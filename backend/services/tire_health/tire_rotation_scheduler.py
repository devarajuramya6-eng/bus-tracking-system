"""
CityBus Enterprise Platform - Tire Rotation & Retreading Lifecycle Scheduler
File: backend/services/tire_health/tire_rotation_scheduler.py

Schedules periodic tire rotation and retreading to maximize casing lifespan:
- Steer axle to drive axle rotation scheduled every 25,000 km
- Retreading inspection milestone when tread depth drops below 3.5 mm (Regrooving / Cold Precured Retread)
"""

from typing import Dict, Any, List


class TireRotationScheduler:
    ROTATION_INTERVAL_KM = 25000.0
    MIN_LEGAL_TREAD_DEPTH_MM = 1.6
    RETREAD_THRESHOLD_DEPTH_MM = 3.2

    @staticmethod
    def audit_tire_set(bus_number: str, current_odometer_km: float, last_rotation_km: float, min_tread_depth_mm: float) -> Dict[str, Any]:
        """
        Determines if tire rotation or retreading work order is required.
        """
        km_since_rotation = current_odometer_km - last_rotation_km
        rotation_due = km_since_rotation >= TireRotationScheduler.ROTATION_INTERVAL_KM
        retread_due = min_tread_depth_mm <= TireRotationScheduler.RETREAD_THRESHOLD_DEPTH_MM
        legal_violation = min_tread_depth_mm <= TireRotationScheduler.MIN_LEGAL_TREAD_DEPTH_MM

        action = 'IMMEDIATE_TIRE_SCRAP_AND_REPLACE' if legal_violation else ('SEND_TO_RETREAD_PLANT' if retread_due else ('SCHEDULE_TIRE_ROTATION' if rotation_due else 'TIRES_HEALTHY'))

        return {
            'bus_number': bus_number,
            'current_odometer_km': current_odometer_km,
            'km_since_last_rotation': km_since_rotation,
            'min_tread_depth_mm': min_tread_depth_mm,
            'is_rotation_overdue': rotation_due,
            'is_retread_required': retread_due,
            'is_below_statutory_limit': legal_violation,
            'maintenance_action': action
        }
