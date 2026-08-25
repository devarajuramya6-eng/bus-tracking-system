"""
CityBus Enterprise Platform - Pedestrian Sidewalk Accessibility Graph
File: backend/services/pedestrian_routing/walk_shed_graph.py

Models pedestrian sidewalk network with barrier-free and heat-resilient routing:
- Accessible curb ramps (Drop kerbs for wheelchairs & strollers)
- Nighttime illumination score (Safe walking routes for female commuters)
- Tree canopy shade index (Penalizes direct sun exposure during 42°C summer days)
"""

from typing import List, Dict, Any, Optional


class SidewalkEdge:
    def __init__(self, u: int, v: int, length_m: float, has_curb_cut: bool = True, is_well_lit: bool = True, shade_score: float = 0.8):
        self.u = u
        self.v = v
        self.length_m = length_m
        self.has_curb_cut = has_curb_cut
        self.is_well_lit = is_well_lit
        self.shade_score = shade_score # 0.0 to 1.0


class PedestrianWalkshedGraph:
    def __init__(self, edges: Optional[List[SidewalkEdge]] = None):
        self.edges = edges or []

    def calculate_path_impedance(self, is_wheelchair: bool = False, is_night: bool = False, is_summer_hot: bool = False) -> List[Dict[str, Any]]:
        """
        Evaluates weighted impedance across pedestrian segments.
        """
        results = []
        for e in self.edges:
            cost = e.length_m

            if is_wheelchair and not e.has_curb_cut:
                cost *= 10.0 # Heavy impedance for non-wheelchair-accessible curbs
            if is_night and not e.is_well_lit:
                cost *= 2.5 # Avoid dark poorly lit alleys at night
            if is_summer_hot:
                cost *= (1.5 - (e.shade_score * 0.5)) # Shaded sidewalks preferred

            results.append({
                'from_node': e.u,
                'to_node': e.v,
                'raw_distance_m': e.length_m,
                'effective_impedance_m': round(cost, 1),
                'is_accessible': e.has_curb_cut if is_wheelchair else True
            })

        return results
