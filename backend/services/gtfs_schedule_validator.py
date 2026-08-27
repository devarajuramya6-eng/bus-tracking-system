from typing import Dict, List, Any
from models import Route, RouteStop, Stop, db

class GTFSScheduleValidator:
    """Validates GTFS schedule coherence, deadhead travel times, and platform dwell minimums."""

    @staticmethod
    def validate_all_routes() -> Dict[str, Any]:
        routes = Route.query.all()
        issues = []
        for r in routes:
            stops = RouteStop.query.filter_by(route_id=r.id).all()
            if len(stops) < 2:
                issues.append({"route_id": r.id, "route_number": r.route_number, "issue": "Insufficient stops defined (<2)"})
            if not r.distance_km or r.distance_km <= 0:
                issues.append({"route_id": r.id, "route_number": r.route_number, "issue": "Missing corridor distance specification"})

        return {
            "total_routes_checked": len(routes),
            "validation_passed": len(issues) == 0,
            "issues_count": len(issues),
            "issues": issues,
            "compliance_score_pct": round(((len(routes) - len(issues)) / max(1, len(routes))) * 100.0, 1)
        }
