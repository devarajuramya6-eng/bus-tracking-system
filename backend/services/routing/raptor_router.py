"""
CityBus Enterprise Platform - Round-Based Public Transit Routing (RAPTOR)
File: backend/services/routing/raptor_router.py

Computes Pareto-optimal transit journeys (Arrival Time vs Number of Transfers):
- Round k computes best arrival times using at most k transit trips
- Pure route-based scanning without edge graphs (Delling et al.)
"""

from typing import List, Dict, Any, Optional, Set


class RAPTORRoute:
    def __init__(self, route_id: int, route_number: str, stops: List[int]):
        self.route_id = route_id
        self.route_number = route_number
        self.stops = stops # List of stop IDs in sequence


class RAPTORRouter:
    """RAPTOR Pareto-optimal journey planning engine."""

    def __init__(self, routes: Optional[List[RAPTORRoute]] = None):
        self.routes = routes or []
        # Index: stop_id -> list of routes serving this stop
        self.stop_to_routes: Dict[int, List[RAPTORRoute]] = {}
        for r in self.routes:
            for s in r.stops:
                if s not in self.stop_to_routes:
                    self.stop_to_routes[s] = []
                self.stop_to_routes[s].append(r)

    def route_query(self, origin_stop: int, dest_stop: int, max_rounds: int = 3) -> List[Dict[str, Any]]:
        """
        Executes RAPTOR algorithm up to max_rounds (transfers).
        """
        # tau_k[k][stop] = earliest arrival time at stop in round k
        pareto_solutions = []
        marked_stops: Set[int] = {origin_stop}
        
        # Simulated standard travel minutes between consecutive stops = 4 min
        stop_dwell_min = 4

        earliest_arrival = {origin_stop: 0} # 0 minutes offset from departure

        for round_k in range(1, max_rounds + 1):
            if not marked_stops:
                break

            # Find routes serving marked stops
            routes_to_scan: Set[RAPTORRoute] = set()
            for s in marked_stops:
                for r in self.stop_to_routes.get(s, []):
                    routes_to_scan.add(r)

            marked_stops = set()

            for route in routes_to_scan:
                boarding_stop = None
                travel_accum = 0

                for stop in route.stops:
                    if boarding_stop is not None:
                        travel_accum += stop_dwell_min
                        arrival_time = earliest_arrival[boarding_stop] + travel_accum

                        if stop not in earliest_arrival or arrival_time < earliest_arrival[stop]:
                            earliest_arrival[stop] = arrival_time
                            marked_stops.add(stop)

                            if stop == dest_stop:
                                pareto_solutions.append({
                                    'transfers': round_k - 1,
                                    'total_travel_minutes': arrival_time,
                                    'route_used': route.route_number
                                })

                    if stop in earliest_arrival:
                        boarding_stop = stop
                        travel_accum = 0

        return sorted(pareto_solutions, key=lambda s: (s['transfers'], s['total_travel_minutes']))
