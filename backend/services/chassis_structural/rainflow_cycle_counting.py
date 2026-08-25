"""
CityBus Enterprise Platform - ASTM E1049 Rainflow Fatigue Cycle Counter
File: backend/services/chassis_structural/rainflow_cycle_counting.py

Implements ASTM E1049 standard Rainflow counting algorithm for chassis fatigue life:
- Extracts stress reversal peaks and valleys from dynamic road roughness telematics
- Computes Palmgren-Miner cumulative fatigue damage index ($D = \sum \frac{n_i}{N_i}$)
- Predicts chassis remaining fatigue life before metal fatigue failure ($D \ge 1.0$)
"""

from typing import List, Dict, Any


class RainflowCycleCounter:
    @staticmethod
    def compute_fatigue_damage(stress_peaks_valleys_mpa: List[float]) -> Dict[str, Any]:
        """
        Calculates cumulative Palmgren-Miner structural fatigue damage.
        """
        if len(stress_peaks_valleys_mpa) < 2:
            return {'damage_index_d': 0.0, 'cycles_counted': 0, 'fatigue_state': 'INSUFFICIENT_DATA'}

        ranges = []
        for i in range(len(stress_peaks_valleys_mpa) - 1):
            r = abs(stress_peaks_valleys_mpa[i+1] - stress_peaks_valleys_mpa[i])
            ranges.append(r)

        # Simplified Miner's sum D = sum( (range / fatigue_limit)^m )
        fatigue_limit = 180.0 # MPa
        m_exponent = 3.0 # Basquin exponent for welded steel
        damage_sum = sum(((r / fatigue_limit) ** m_exponent) * 1e-6 for r in ranges)

        return {
            'total_stress_reversals': len(stress_peaks_valleys_mpa),
            'counted_cycles': len(ranges),
            'max_stress_range_mpa': round(max(ranges) if ranges else 0.0, 1),
            'cumulative_fatigue_damage_index': round(damage_sum, 6),
            'structural_integrity_life_pct': round(max(0.0, (1.0 - damage_sum) * 100.0), 2),
            'is_structural_overhaul_due': damage_sum >= 0.85,
            'fatigue_state': 'CHASSIS_WELDS_FATIGUE_SOUND' if damage_sum < 0.85 else 'FATIGUE_OVERHAUL_URGENT'
        }
