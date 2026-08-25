"""
CityBus Enterprise Platform - Depot Spare Parts Inventory & Reorder Optimizer
File: backend/services/maintenance_ops/spare_parts_inventory.py

Manages central transit depot spare parts warehouse inventory:
- Economic Order Quantity (EOQ) optimization
- Safety stock levels & automated reorder point (ROP) calculation
- Lead time buffer and stockout risk mitigation
"""

import math
from typing import Dict, Any, List


class SparePartsInventoryEngine:
    PARTS_CATALOG = [
        {'part_number': 'BRK-LIN-01', 'name': 'Heavy Duty Front Brake Lining Set', 'unit_cost': 3450.0, 'stock_on_hand': 14, 'min_safety_stock': 20, 'annual_demand': 180, 'holding_cost': 350.0, 'order_cost': 1200.0, 'lead_days': 5},
        {'part_number': 'TIR-295-80', 'name': 'Radial Transit Bus Tire 295/80R22.5', 'unit_cost': 18500.0, 'stock_on_hand': 8, 'min_safety_stock': 12, 'annual_demand': 120, 'holding_cost': 1800.0, 'order_cost': 2500.0, 'lead_days': 7},
        {'part_number': 'FLT-OIL-HD', 'name': 'Cummins ISB6.7 Engine Oil Filter', 'unit_cost': 680.0, 'stock_on_hand': 45, 'min_safety_stock': 30, 'annual_demand': 360, 'holding_cost': 70.0, 'order_cost': 500.0, 'lead_days': 3},
        {'part_number': 'EV-CON-120', 'name': 'CCS2 DC Fast Charging Gun & Cable', 'unit_cost': 42000.0, 'stock_on_hand': 2, 'min_safety_stock': 3, 'annual_demand': 10, 'holding_cost': 4200.0, 'order_cost': 5000.0, 'lead_days': 14}
    ]

    @staticmethod
    def calculate_eoq_and_status() -> List[Dict[str, Any]]:
        """
        Calculates EOQ = sqrt((2 * Demand * OrderCost) / HoldingCost) and flags reorder items.
        """
        results = []
        for p in SparePartsInventoryEngine.PARTS_CATALOG:
            d = p['annual_demand']
            s = p['order_cost']
            h = p['holding_cost']

            eoq = int(round(math.sqrt((2 * d * s) / h))) if h > 0 else 10
            is_reorder_needed = p['stock_on_hand'] <= p['min_safety_stock']

            results.append({
                'part_number': p['part_number'],
                'name': p['name'],
                'unit_cost_inr': p['unit_cost'],
                'stock_on_hand': p['stock_on_hand'],
                'min_safety_stock': p['min_safety_stock'],
                'eoq_quantity': eoq,
                'is_reorder_needed': is_reorder_needed,
                'reorder_status': 'CRITICAL_REORDER' if is_reorder_needed else 'STOCKED',
                'lead_days': p['lead_days']
            })

        return results
