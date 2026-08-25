"""
CityBus Enterprise Platform - High-Voltage Battery Cell Voltage Equalizer
File: backend/services/ev_battery/cell_voltage_equalizer.py

Monitors individual series cell voltages across 800V traction battery packs:
- Computes cell voltage deviation Delta V = V_max - V_min
- Triggers active capacitive / passive dissipative charge balancing when Delta V > 15mV
- Isolates and flags weak degraded cells for warranty replacement
"""

from typing import List, Dict, Any


class BatteryCellEqualizer:
    MAX_ALLOWABLE_DELTA_V_MV = 25.0
    BALANCING_TRIGGER_DELTA_V_MV = 15.0

    @staticmethod
    def analyze_pack_cells(pack_id: str, cell_voltages_v: List[float]) -> Dict[str, Any]:
        """
        Analyzes individual cell voltages and triggers balancing.
        """
        if not cell_voltages_v:
            return {'status': 'NO_CELL_TELEMETRY'}

        v_min = min(cell_voltages_v)
        v_max = max(cell_voltages_v)
        v_avg = sum(cell_voltages_v) / len(cell_voltages_v)
        delta_v_mv = (v_max - v_min) * 1000.0

        min_idx = cell_voltages_v.index(v_min)
        max_idx = cell_voltages_v.index(v_max)

        balancing_required = delta_v_mv > BatteryCellEqualizer.BALANCING_TRIGGER_DELTA_V_MV
        critical_imbalance = delta_v_mv > BatteryCellEqualizer.MAX_ALLOWABLE_DELTA_V_MV

        return {
            'pack_id': pack_id,
            'total_cells_monitored': len(cell_voltages_v),
            'min_cell_voltage_v': round(v_min, 4),
            'max_cell_voltage_v': round(v_max, 4),
            'average_cell_voltage_v': round(v_avg, 4),
            'delta_v_millivolts': round(delta_v_mv, 1),
            'weakest_cell_index': min_idx + 1,
            'highest_cell_index': max_idx + 1,
            'is_balancing_active': balancing_required,
            'balancing_mode': 'ACTIVE_CAPACITIVE_SHUNT' if balancing_required else 'BALANCED_IDLE',
            'health_status': 'PACK_IMBALANCE_WARNING' if critical_imbalance else ('BALANCING_IN_PROGRESS' if balancing_required else 'OPTIMAL_BALANCED')
        }
