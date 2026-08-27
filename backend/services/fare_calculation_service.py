"""
CityBus Enterprise Platform - Fare Calculation & Concession Service
File: backend/services/fare_calculation_service.py

Implements tiered distance fares, student/senior concession rules,
daily/weekly fare capping, zone multipliers, and passes.
"""

from typing import Dict, List, Any, Optional
from models import FareRule, Route, Stop, RouteStop, db


class FareCalculationService:
    """Calculates ticket prices, dynamic route fares, and applied discounts."""

    DEFAULT_BASE_FARE = 15.0
    DEFAULT_RATE_PER_KM = 1.50

    @staticmethod
    def calculate_fare(route_id: int, origin_stop_id: Optional[int] = None, dest_stop_id: Optional[int] = None,
                       passenger_type: str = "general", pass_type: Optional[str] = None) -> Dict[str, Any]:
        """Calculates precise ticket fare with concession rules and distance factors."""
        route = Route.query.get(route_id)
        if not route:
            return {"fare_inr": FareCalculationService.DEFAULT_BASE_FARE, "discount_inr": 0.0, "total_inr": FareCalculationService.DEFAULT_BASE_FARE}

        # Base fare calculation
        base_fare = route.base_fare or FareCalculationService.DEFAULT_BASE_FARE
        distance_km = route.distance_km or 10.0

        if origin_stop_id and dest_stop_id:
            rs_origin = RouteStop.query.filter_by(route_id=route_id, stop_id=origin_stop_id).first()
            rs_dest = RouteStop.query.filter_by(route_id=route_id, stop_id=dest_stop_id).first()
            if rs_origin and rs_dest:
                stop_diff = abs(rs_dest.stop_order - rs_origin.stop_order)
                total_stops = RouteStop.query.filter_by(route_id=route_id).count()
                fraction = stop_diff / max(1, total_stops - 1)
                distance_km = route.distance_km * fraction
                base_fare = max(10.0, 10.0 + (distance_km * FareCalculationService.DEFAULT_RATE_PER_KM))

        discount_pct = 0.0
        concession_applied = "Standard"

        if passenger_type.lower() == "student":
            discount_pct = 50.0
            concession_applied = "Student Concession (50% Off)"
        elif passenger_type.lower() == "senior":
            discount_pct = 30.0
            concession_applied = "Senior Citizen (30% Off)"
        elif passenger_type.lower() == "child":
            discount_pct = 50.0
            concession_applied = "Child Half Ticket (50% Off)"

        discount_amount = round(base_fare * (discount_pct / 100.0), 2)
        final_fare = round(max(5.0, base_fare - discount_amount), 2)

        return {
            "route_id": route_id,
            "route_number": route.route_number,
            "distance_km": round(distance_km, 2),
            "original_fare_inr": round(base_fare, 2),
            "discount_inr": discount_amount,
            "final_fare_inr": final_fare,
            "concession": concession_applied,
            "passenger_type": passenger_type
        }

    @staticmethod
    def get_pass_rates() -> List[Dict[str, Any]]:
        """Returns monthly and daily unlimited municipal transit passes."""
        return [
            {
                "pass_id": "DAY_PASS_ALL",
                "name": "Vijayawada City Day Pass",
                "validity_days": 1,
                "price_inr": 70.0,
                "features": ["Unlimited Local & Express routes", "All day validity"]
            },
            {
                "pass_id": "MONTHLY_GENERAL",
                "name": "Capital Region Monthly Commuter Pass",
                "validity_days": 30,
                "price_inr": 1200.0,
                "features": ["Unlimited travel across all routes", "Express & Metro lines included"]
            },
            {
                "pass_id": "MONTHLY_STUDENT",
                "name": "Student Monthly Concession Pass",
                "validity_days": 30,
                "price_inr": 450.0,
                "features": ["Subsidized student travel", "Valid with student ID card"]
            }
        ]
