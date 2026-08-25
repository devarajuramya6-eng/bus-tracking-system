"""
CityBus Enterprise Platform - Route Profitability & Cost Per KM (CPKM) Matrix
File: backend/services/network_performance/route_profitability_matrix.py

Computes commercial corridor profitability and municipal subsidy requirements:
- EPKM (Earnings Per Kilometer) = Total Revenue / Total Kilometers
- CPKM (Cost Per Kilometer) = (Fuel/Power + Driver Crew Wages + Maintenance Depreciation) / Total Kilometers
- Operating Ratio (OR) = (CPKM / EPKM) * 100
"""

from typing import Dict, Any, List


class RouteProfitabilityAnalyzer:
    DEFAULT_DIESEL_CPKM_INR = 48.50
    DEFAULT_ELECTRIC_CPKM_INR = 34.20 # Lower energy + maintenance costs for EV

    @staticmethod
    def evaluate_route_economics(route_number: str, total_revenue_inr: float,
                                 total_distance_km: float, is_electric: bool = False) -> Dict[str, Any]:
        """
        Calculates EPKM, CPKM, Operating Ratio, and Net Profit Margin.
        """
        epkm = total_revenue_inr / max(1.0, total_distance_km)
        cpkm = RouteProfitabilityAnalyzer.DEFAULT_ELECTRIC_CPKM_INR if is_electric else RouteProfitabilityAnalyzer.DEFAULT_DIESEL_CPKM_INR
        total_operating_cost = cpkm * total_distance_km

        net_profit_loss = total_revenue_inr - total_operating_cost
        operating_ratio = (cpkm / max(1.0, epkm)) * 100.0

        is_profitable = epkm >= cpkm

        return {
            'route_number': route_number,
            'is_electric_fleet': is_electric,
            'total_distance_km': round(total_distance_km, 1),
            'total_revenue_inr': round(total_revenue_inr, 2),
            'total_operating_cost_inr': round(total_operating_cost, 2),
            'earnings_per_km_epkm': round(epkm, 2),
            'cost_per_km_cpkm': round(cpkm, 2),
            'net_profit_or_loss_inr': round(net_profit_loss, 2),
            'operating_ratio_pct': round(operating_ratio, 1),
            'commercial_viability': 'PROFITABLE_COMMERCIAL' if is_profitable else 'REQUIRES_PUBLIC_PSO_SUBSIDY'
        }
