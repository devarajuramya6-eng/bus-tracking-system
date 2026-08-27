"""
CityBus Enterprise Platform - Transit Network Graph Builder & Pathfinding
File: backend/services/network_graph_builder.py

Builds spatial adjacency graphs with Dijkstra / A* heuristics, calculates
transfer penalty weights, walking interchange connectors, and multi-criteria journey costs.
"""

import math
import heapq
from typing import Dict, List, Any, Optional, Tuple, Set
from models import Route, Stop, RouteStop, db


class NetworkGraphNode:
    def __init__(self, stop_id: int, name: str, lat: float, lng: float):
        self.stop_id = stop_id
        self.name = name
        self.lat = lat
        self.lng = lng
        # Edges: target_stop_id -> List of (weight_minutes, route_id, route_number, mode)
        self.edges: Dict[int, List[Tuple[float, int, str, str]]] = {}


class NetworkGraphBuilder:
    """Constructs multi-modal transit network topology from SQL models."""

    def __init__(self):
        self.nodes: Dict[int, NetworkGraphNode] = {}
        self.is_built = False

    @staticmethod
    def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lng / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return 6371.0 * c

    def build(self):
        """Loads all stops and route sequences into the directed graph."""
        self.nodes.clear()
        stops = Stop.query.all()
        for s in stops:
            self.nodes[s.id] = NetworkGraphNode(s.id, s.name, s.latitude, s.longitude)

        # Build route edges
        routes = Route.query.all()
        for r in routes:
            route_stops = RouteStop.query.filter_by(route_id=r.id).order_by(RouteStop.stop_order.asc()).all()
            for i in range(len(route_stops) - 1):
                u_id = route_stops[i].stop_id
                v_id = route_stops[i + 1].stop_id

                if u_id in self.nodes and v_id in self.nodes:
                    u_node = self.nodes[u_id]
                    v_node = self.nodes[v_id]

                    dist_km = self.haversine_km(u_node.lat, u_node.lng, v_node.lat, v_node.lng)
                    travel_time_min = max(2.0, (dist_km / 30.0) * 60.0) # 30 km/h avg bus speed

                    if v_id not in u_node.edges:
                        u_node.edges[v_id] = []
                    u_node.edges[v_id].append((travel_time_min, r.id, r.route_number, "BUS"))

        # Add walking transfer edges between stops within 400m
        stop_list = list(self.nodes.values())
        for i in range(len(stop_list)):
            for j in range(i + 1, len(stop_list)):
                s1 = stop_list[i]
                s2 = stop_list[j]
                d_km = self.haversine_km(s1.lat, s1.lng, s2.lat, s2.lng)
                if d_km <= 0.4: # 400 meters interchange threshold
                    walk_time_min = (d_km / 4.5) * 60.0 # 4.5 km/h walking speed
                    if s2.stop_id not in s1.edges: s1.edges[s2.stop_id] = []
                    if s1.stop_id not in s2.edges: s2.edges[s1.stop_id] = []
                    s1.edges[s2.stop_id].append((walk_time_min, 0, "WALK", "WALK"))
                    s2.edges[s1.stop_id].append((walk_time_min, 0, "WALK", "WALK"))

        self.is_built = True

    def find_shortest_path(self, origin_stop_id: int, dest_stop_id: int) -> Optional[Dict[str, Any]]:
        """Executes Dijkstra search to find minimum-duration path."""
        if not self.is_built:
            self.build()

        if origin_stop_id not in self.nodes or dest_stop_id not in self.nodes:
            return None

        # Priority Queue: (cumulative_minutes, current_stop_id, path_history)
        pq: List[Tuple[float, int, List[Any]]] = [(0.0, origin_stop_id, [])]
        best_times: Dict[int, float] = {origin_stop_id: 0.0}

        while pq:
            curr_time, curr_stop, path = heapq.heappop(pq)

            if curr_stop == dest_stop_id:
                return {
                    "origin_stop_id": origin_stop_id,
                    "dest_stop_id": dest_stop_id,
                    "total_duration_minutes": round(curr_time, 1),
                    "steps": path
                }

            if curr_time > best_times.get(curr_stop, float('inf')):
                continue

            node = self.nodes[curr_stop]
            for next_stop, edge_list in node.edges.items():
                for weight_min, route_id, route_num, mode in edge_list:
                    # Transfer penalty: +4 minutes if switching routes
                    transfer_penalty = 4.0 if (path and path[-1].get('route_id') != route_id and mode == "BUS") else 0.0
                    new_time = curr_time + weight_min + transfer_penalty

                    if new_time < best_times.get(next_stop, float('inf')):
                        best_times[next_stop] = new_time
                        new_step = {
                            "from_stop": node.name,
                            "to_stop": self.nodes[next_stop].name,
                            "mode": mode,
                            "route_number": route_num,
                            "route_id": route_id,
                            "segment_duration_min": round(weight_min, 1)
                        }
                        heapq.heappush(pq, (new_time, next_stop, path + [new_step]))

        return None
