"""
CityBus Enterprise Platform - Electronic Brake Pad & Lining Wear Sensor
File: backend/services/tire_health/brake_lining_wear_sensor.py

Monitors electronic brake lining wear sensors (BWI) across all axles:
- New pad thickness: 22.0 mm
- Service warning threshold: 5.0 mm remaining (22% life)
- Critical metal-on-metal danger threshold: 2.0 mm remaining (Immediate work order)
"""

from typing import Dict, Any


class BrakeLiningWearMonitor:
    NEW_PAD_THICKNESS_MM = 22.0
    WARNING_THRESHOLD_MM = 5.0
    CRITICAL_THRESHOLD_MM = 2.0

    @staticmethod
    def evaluate_brake_wear(axle_name: str, pad_thickness_mm: float, avg_wear_mm_per_10k_km: float = 1.2) -> Dict[str, Any]:
        """
        Evaluates remaining brake lining thickness and predicts replacement mileage.
        """
        usable_material_mm = max(0.0, pad_thickness_mm - BrakeLiningWearMonitor.CRITICAL_THRESHOLD_MM)
        remaining_km_est = int((usable_material_mm / max(0.1, avg_wear_mm_per_10k_km)) * 10000.0)
        wear_pct = max(0.0, min(100.0, ((BrakeLiningWearMonitor.NEW_PAD_THICKNESS_MM - pad_thickness_mm) / BrakeLiningWearMonitor.NEW_PAD_THICKNESS_MM) * 100.0))

        is_critical = pad_thickness_mm <= BrakeLiningWearMonitor.CRITICAL_THRESHOLD_MM
        is_warning = pad_thickness_mm <= BrakeLiningWearMonitor.WARNING_THRESHOLD_MM

        status = 'CRITICAL_REPLACE_IMMEDIATELY' if is_critical else ('SCHEDULE_PAD_REPLACEMENT' if is_warning else 'NOMINAL_GOOD')

        return {
            'axle_name': axle_name,
            'current_pad_thickness_mm': round(pad_thickness_mm, 1),
            'wear_percentage': round(wear_pct, 1),
            'remaining_distance_km_est': remaining_km_est,
            'is_wear_warning': is_warning,
            'is_critical_danger': is_critical,
            'maintenance_status': status
        }
