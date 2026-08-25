"""
CityBus Enterprise Platform - Driver Roster Fairness Gini Coefficient Engine
File: backend/services/driver_rostering/shift_fairness_gini_coefficient.py

Measures statistical equity in duty assignments (Overtime, Weekend, and Night Shifts):
- Computes Gini Coefficient (0.00 = Perfect Equality, 1.00 = Extreme Disparity)
- Target Gini index: < 0.18 (Ensures fair distribution of arduous night routes)
"""

from typing import List, Dict, Any


class ShiftFairnessGiniCalculator:
    @staticmethod
    def calculate_workload_gini(driver_hours_list: List[float]) -> Dict[str, Any]:
        """
        Calculates Gini coefficient across driver hours.
        """
        n = len(driver_hours_list)
        if n <= 1:
            return {'gini_coefficient': 0.0, 'is_equitable': True, 'total_drivers': n}

        sorted_hours = sorted(driver_hours_list)
        total_hours = sum(sorted_hours)
        mean_hours = total_hours / n

        if mean_hours == 0:
            return {'gini_coefficient': 0.0, 'is_equitable': True, 'total_drivers': n}

        # Gini = sum_i ((2i - n - 1) * x_i) / (n * sum(x))
        numerator = sum((2 * (i + 1) - n - 1) * sorted_hours[i] for i in range(n))
        gini = numerator / (n * total_hours)
        gini = max(0.0, min(1.0, gini))

        is_fair = gini <= 0.20

        return {
            'total_drivers_evaluated': n,
            'mean_driver_hours': round(mean_hours, 1),
            'gini_coefficient': round(gini, 3),
            'is_equitable': is_fair,
            'union_equity_grade': 'EXCELLENT_EQUITY' if gini < 0.12 else ('ACCEPTABLE' if is_fair else 'HIGH_DISPARITY_AUDIT_RECOMMENDED')
        }
