"""
CityBus Enterprise Platform - Depot Fuel Stockout Runway Predictor
File: backend/services/fuel_logistics/fuel_stockout_predictor.py

Predicts depot fuel inventory days of supply:
- Moving average daily fleet diesel burn rate (Liters/day)
- Reorder point calculation: Lead time (2 days) * Daily Burn + Safety Buffer (3,000 L)
- Automated Electronic Purchase Indent generation to Oil Marketing Companies (OMCs)
"""

from typing import Dict, Any


class FuelStockoutPredictor:
    LEAD_TIME_DAYS = 2
    SAFETY_STOCK_LITERS = 4000.0

    @staticmethod
    def predict_stockout(current_inventory_liters: float, avg_daily_consumption_liters: float = 3800.0) -> Dict[str, Any]:
        """
        Calculates remaining days of supply and indent requirement.
        """
        days_remaining = current_inventory_liters / max(1.0, avg_daily_consumption_liters)
        reorder_trigger_volume = (FuelStockoutPredictor.LEAD_TIME_DAYS * avg_daily_consumption_liters) + FuelStockoutPredictor.SAFETY_STOCK_LITERS

        reorder_needed = current_inventory_liters <= reorder_trigger_volume

        return {
            'current_inventory_liters': round(current_inventory_liters, 1),
            'avg_daily_burn_liters': round(avg_daily_consumption_liters, 1),
            'days_of_supply_remaining': round(days_remaining, 1),
            'reorder_point_liters': round(reorder_trigger_volume, 1),
            'is_purchase_indent_required': reorder_needed,
            'recommended_order_quantity_liters': 20000.0 if reorder_needed else 0.0,
            'inventory_status': 'CRITICAL_REORDER_NOW' if days_remaining <= 2.0 else ('REORDER_SOON' if reorder_needed else 'HEALTHY_STOCK')
        }
