"""
CityBus Enterprise Platform - Fleet Asset Lifecycle & Capital Depreciation Service
File: backend/services/fleet_lifecycle_depreciation.py

Calculates 10-year straight-line depreciation, book salvage value, battery pack replacement amortization,
and Total Cost of Ownership (TCO) comparisons between Diesel and Electric fleets.
"""

from typing import Dict, List, Any, Optional
from models import Bus, db


class FleetLifecycleDepreciation:
    """Calculates municipal accounting asset depreciation and TCO schedules."""

    DIESEL_BUS_CAPEX_INR = 4500000.0  # ₹45 Lakh
    EV_BUS_CAPEX_INR = 12000000.0     # ₹1.2 Crore
    LIFESPAN_YEARS = 10
    SALVAGE_VALUE_PCT = 10.0          # 10% residual value after 10 years

    @staticmethod
    def calculate_vehicle_book_value(bus_id: int, age_years: float = 3.5) -> Dict[str, Any]:
        """Calculates current depreciated balance sheet value."""
        bus = Bus.query.get(bus_id)
        if not bus:
            return {"error": "Bus not found"}

        is_ev = bus.fuel_type == "Electric"
        initial_cost = FleetLifecycleDepreciation.EV_BUS_CAPEX_INR if is_ev else FleetLifecycleDepreciation.DIESEL_BUS_CAPEX_INR
        salvage = initial_cost * (FleetLifecycleDepreciation.SALVAGE_VALUE_PCT / 100.0)
        depreciable_base = initial_cost - salvage

        annual_depreciation = depreciable_base / FleetLifecycleDepreciation.LIFESPAN_YEARS
        accumulated_depreciation = min(depreciable_base, round(annual_depreciation * age_years, 2))
        current_book_value = round(initial_cost - accumulated_depreciation, 2)

        return {
            "bus_id": bus.id,
            "bus_number": bus.bus_number,
            "fuel_type": bus.fuel_type,
            "initial_acquisition_cost_inr": initial_cost,
            "vehicle_age_years": age_years,
            "annual_depreciation_inr": round(annual_depreciation, 2),
            "accumulated_depreciation_inr": accumulated_depreciation,
            "current_book_value_inr": current_book_value,
            "salvage_residual_value_inr": salvage
        }
