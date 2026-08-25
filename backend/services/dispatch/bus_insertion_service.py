"""
CityBus Enterprise Platform - Standby Bus Insertion & Short-Turning Service
File: backend/services/dispatch/bus_insertion_service.py

Manages rapid tactical interventions when a vehicle breaks down or encounters extreme delays:
- Standby Depot Bus Injection: Dispatches reserve buses from closest depot
- Short-Turning Optimization: Commands delayed buses to reverse direction at intermediate crossover points
"""

from typing import List, Dict, Any
from repositories.bus_repository import BusRepository


class BusInsertionService:
    DEPOT_STANDBY_INVENTORY = {
        'PNBS_CENTRAL': [{'bus_id': 101, 'bus_number': 'AP16-Z-9001', 'type': 'Electric AC'}, {'bus_id': 102, 'bus_number': 'AP16-Z-9002', 'type': 'Express Diesel'}],
        'AUTONAGAR_DEPOT': [{'bus_id': 103, 'bus_number': 'AP16-Z-9003', 'type': 'Standard Diesel'}],
        'MANGALAGIRI_DEPOT': [{'bus_id': 104, 'bus_number': 'AP16-Z-9004', 'type': 'Electric AC'}]
    }

    @staticmethod
    def recommend_insertion(incident_lat: float, incident_lng: float, route_id: int) -> Dict[str, Any]:
        """
        Finds the closest standby reserve bus to inject into the corridor.
        """
        best_depot = 'PNBS_CENTRAL'
        min_dist = float('inf')

        depot_coords = {
            'PNBS_CENTRAL': (16.5100, 80.6175),
            'AUTONAGAR_DEPOT': (16.4950, 80.6780),
            'MANGALAGIRI_DEPOT': (16.4350, 80.5700)
        }

        for depot, coords in depot_coords.items():
            dist = BusRepository.haversine_km(incident_lat, incident_lng, coords[0], coords[1])
            if dist < min_dist:
                min_dist = dist
                best_depot = depot

        standby_list = BusInsertionService.DEPOT_STANDBY_INVENTORY.get(best_depot, [])
        assigned_bus = standby_list[0] if standby_list else {'bus_number': 'AP16-Z-RESERVE', 'type': 'Standard'}

        return {
            'status': 'STANDBY_DISPATCH_RECOMMENDED',
            'recommended_depot': best_depot,
            'distance_to_incident_km': round(min_dist, 2),
            'estimated_arrival_minutes': int((min_dist / 35.0) * 60.0 + 5),
            'assigned_standby_vehicle': assigned_bus,
            'action_plan': f"Dispatch reserve vehicle {assigned_bus['bus_number']} from {best_depot} to cover corridor gap."
        }
