"""
CityBus Enterprise Platform - Excess Wait Time (EWT) High-Frequency Route Quality Engine
File: backend/services/network_performance/excess_wait_time_ewt.py

Calculates Excess Wait Time (EWT) for high-frequency headway corridors (Transport for London standard):
- Average Scheduled Wait Time (SWT) = Sum(h_sched^2) / (2 * Sum(h_sched))
- Average Actual Wait Time (AWT) = Sum(h_actual^2) / (2 * Sum(h_actual))
- Excess Wait Time (EWT) = AWT - SWT (Measures passenger frustration caused by bus bunching)
"""

from typing import List, Dict, Any


class ExcessWaitTimeCalculator:
    @staticmethod
    def calculate_ewt(scheduled_headways_min: List[float], actual_headways_min: List[float]) -> Dict[str, Any]:
        """
        Calculates TfL standard Excess Wait Time (EWT).
        """
        if not scheduled_headways_min or not actual_headways_min:
            return {'status': 'EMPTY_HEADWAY_SERIES'}

        # SWT = sum(h^2) / (2 * sum(h))
        sum_sq_sched = sum(h * h for h in scheduled_headways_min)
        sum_sched = sum(scheduled_headways_min)
        swt = sum_sq_sched / (2.0 * max(0.1, sum_sched))

        # AWT = sum(h^2) / (2 * sum(h))
        sum_sq_actual = sum(h * h for h in actual_headways_min)
        sum_actual = sum(actual_headways_min)
        awt = sum_sq_actual / (2.0 * max(0.1, sum_actual))

        ewt = max(0.0, awt - swt)

        return {
            'scheduled_wait_time_min': round(swt, 2),
            'actual_wait_time_min': round(awt, 2),
            'excess_wait_time_min': round(ewt, 2),
            'headway_irregularity_score': round(ewt / max(0.1, swt), 2),
            'quality_of_service': 'OUTSTANDING' if ewt < 0.8 else ('ACCEPTABLE' if ewt < 1.5 else 'POOR_BUNCHING_DETECTED')
        }
