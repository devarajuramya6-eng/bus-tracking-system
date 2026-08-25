"""
CityBus Enterprise Platform - Tire Retread Lifecycle Cost-Per-KM (CPKM) ROI Model
File: backend/services/retread_ndt/retread_lifecycle_roi_model.py

Evaluates multi-lifecycle financial savings from cold precured retreading:
- New Tire Cost: ₹24,000 (Yields ~100,000 km = ₹0.24 / km)
- Retread 1 Cost: ₹4,500 (Yields ~80,000 km = ₹0.056 / km)
- Retread 2 Cost: ₹4,500 (Yields ~75,000 km = ₹0.060 / km)
- Combined Multi-Life CPKM: ₹0.13 / km (46% net operating savings)
"""

from typing import Dict, Any


class RetreadLifecycleROIModel:
    NEW_TIRE_COST_INR = 24000.0
    RETREAD_COST_INR = 4500.0

    @staticmethod
    def calculate_casing_lifecycle_cpkm(retread_count: int = 2) -> Dict[str, Any]:
        """
        Calculates total lifecycle mileage, cost, and CPKM.
        """
        total_cost = RetreadLifecycleROIModel.NEW_TIRE_COST_INR + (retread_count * RetreadLifecycleROIModel.RETREAD_COST_INR)
        total_km = 100000.0 + (retread_count * 75000.0)

        cpkm = total_cost / total_km
        new_tire_only_cpkm = RetreadLifecycleROIModel.NEW_TIRE_COST_INR / 100000.0

        savings_pct = ((new_tire_only_cpkm - cpkm) / new_tire_only_cpkm) * 100.0

        return {
            'total_retreads': retread_count,
            'total_lifecycle_investment_inr': round(total_cost, 2),
            'total_expected_mileage_km': round(total_km, 1),
            'lifecycle_cpkm_inr': round(cpkm, 4),
            'baseline_new_tire_cpkm_inr': round(new_tire_only_cpkm, 4),
            'operating_cost_savings_pct': round(savings_pct, 1)
        }
