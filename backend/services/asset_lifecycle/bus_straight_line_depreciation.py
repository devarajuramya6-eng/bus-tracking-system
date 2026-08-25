"""
CityBus Enterprise Platform - Fleet Asset Straight-Line & WDV Depreciation Engine
File: backend/services/asset_lifecycle/bus_straight_line_depreciation.py

Calculates asset depreciation per Indian Companies Act Schedule II / Municipal Accounting Standards:
- Bus Chassis & Body: 12-Year useful lifespan (10% residual salvage value)
- EV Traction Battery: 8-Year useful lifespan (15% second-life grid storage salvage value)
- Computes Annual Depreciation, Accumulated Depreciation, and Current Net Book Value (NBV)
"""

from typing import Dict, Any


class FleetDepreciationCalculator:
    BUS_USEFUL_LIFE_YEARS = 12
    BUS_SALVAGE_VALUE_PCT = 0.10

    BATTERY_USEFUL_LIFE_YEARS = 8
    BATTERY_SALVAGE_VALUE_PCT = 0.15

    @staticmethod
    def calculate_bus_asset_value(purchase_price_inr: float, age_years: float, is_battery_pack: bool = False) -> Dict[str, Any]:
        """
        Calculates straight-line depreciation and current book value.
        """
        useful_life = FleetDepreciationCalculator.BATTERY_USEFUL_LIFE_YEARS if is_battery_pack else FleetDepreciationCalculator.BUS_USEFUL_LIFE_YEARS
        salvage_pct = FleetDepreciationCalculator.BATTERY_SALVAGE_VALUE_PCT if is_battery_pack else FleetDepreciationCalculator.BUS_SALVAGE_VALUE_PCT

        salvage_value = purchase_price_inr * salvage_pct
        depreciable_base = purchase_price_inr - salvage_value
        annual_depreciation = depreciable_base / useful_life

        clamped_age = min(useful_life, max(0.0, age_years))
        accumulated_depreciation = annual_depreciation * clamped_age
        net_book_value = max(salvage_value, purchase_price_inr - accumulated_depreciation)

        return {
            'purchase_price_inr': round(purchase_price_inr, 2),
            'asset_age_years': round(age_years, 2),
            'useful_life_years': useful_life,
            'salvage_value_inr': round(salvage_value, 2),
            'annual_depreciation_inr': round(annual_depreciation, 2),
            'accumulated_depreciation_inr': round(accumulated_depreciation, 2),
            'net_book_value_inr': round(net_book_value, 2),
            'is_fully_depreciated': age_years >= useful_life
        }
