"""
CityBus Enterprise Platform - Dynamic Fleet & Route Rebalancing Service
File: backend/services/route_rebalancing_service.py

Monitors real-time passenger surge demand at key interchange terminals,
calculates route deficit indices, and triggers short-turning or depot extra bus injections.
"""

from typing import Dict, List, Any, Optional
from models import Bus, Route, Stop, db
from repositories.audit_repository import AuditRepository


class RouteRebalancingService:
    """Calculates corridor demand pressure and recommends dynamic fleet reallocations."""

    @staticmethod
    def evaluate_corridor_rebalancing() -> List[Dict[str, Any]]:
        """Scans all transit corridors to identify overcrowded vs under-utilized routes."""
        routes = Route.query.all()
        recommendations = []

        for r in routes:
            buses = Bus.query.filter_by(route_id=r.id).all()
            if not buses:
                continue

            total_occ = sum(b.occupancy for b in buses)
            total_cap = sum(b.capacity for b in buses)
            utilization_rate = (total_occ / max(1, total_cap)) * 100.0

            if utilization_rate > 85.0:
                recommendations.append({
                    "route_id": r.id,
                    "route_number": r.route_number,
                    "name": r.name,
                    "utilization_pct": round(utilization_rate, 1),
                    "action_required": "INJECT_RESERVE_BUS",
                    "priority": "HIGH",
                    "recommendation": f"Deploy 1 reserve bus from depot to {r.route_number} to alleviate surge."
                })
            elif utilization_rate < 25.0 and len(buses) > 3:
                recommendations.append({
                    "route_id": r.id,
                    "route_number": r.route_number,
                    "name": r.name,
                    "utilization_pct": round(utilization_rate, 1),
                    "action_required": "EXTEND_HEADWAY_OR_REASSIGN",
                    "priority": "LOW",
                    "recommendation": f"Reallocate 1 bus from {r.route_number} to high-density arterial line."
                })

        return recommendations
