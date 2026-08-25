"""
CityBus Enterprise Platform - Technician Labor Productivity & Standard Repair Time (SRT)
File: backend/services/maintenance_erp/mechanic_labor_productivity.py

Evaluates workshop technician repair speed and productivity:
- Compares actual clock hours against Standard Repair Times (SRT) (e.g. Brake pad change = 2.5 hrs)
- Efficiency ratio = (Billed SRT Hours / Actual Clocked Hours) * 100
"""

from typing import Dict, Any


class MechanicLaborProductivity:
    STANDARD_REPAIR_TIMES_HOURS = {
        'BRAKE_PAD_REPLACEMENT_ALL': 2.5,
        'OIL_AND_FILTER_CHANGE': 1.0,
        'CLUTCH_PLATE_OVERHAUL': 4.5,
        'EV_BATTERY_COOLANT_FLUSH': 2.0,
        'ALTERNATOR_REPLACE': 1.5
    }

    @staticmethod
    def calculate_technician_efficiency(technician_id: int, job_type: str, actual_hours: float) -> Dict[str, Any]:
        """
        Calculates labor efficiency ratio.
        """
        srt = MechanicLaborProductivity.STANDARD_REPAIR_TIMES_HOURS.get(job_type, 2.0)
        efficiency_pct = (srt / max(0.25, actual_hours)) * 100.0

        if efficiency_pct >= 110.0:
            rating = 'EXCEEDS_BENCHMARK'
        elif efficiency_pct >= 90.0:
            rating = 'ON_BENCHMARK'
        else:
            rating = 'TRAINING_REQUIRED'

        return {
            'technician_id': technician_id,
            'job_type': job_type,
            'standard_repair_time_hours': srt,
            'actual_hours_taken': round(actual_hours, 2),
            'labor_efficiency_percentage': round(efficiency_pct, 1),
            'productivity_rating': rating
        }
