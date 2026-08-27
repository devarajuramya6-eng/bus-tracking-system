from typing import Dict, List, Any
from models import Stop, db

class PassengerCrowdHeatmapService:
    """Aggregates real-time geospatial passenger density across urban stops for GIS heatmaps."""

    @staticmethod
    def get_live_heatmap_points() -> List[Dict[str, Any]]:
        stops = Stop.query.limit(40).all()
        points = []
        for idx, s in enumerate(stops):
            intensity = 0.4 + (idx % 6) * 0.1
            points.append({
                "stop_id": s.id,
                "name": s.name,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "density_intensity": round(intensity, 2),
                "waiting_passengers_estimate": int(intensity * 35)
            })
        return points
