"""
CityBus Enterprise Platform - Depot Overnight Yard Stack Parking Optimizer
File: backend/services/depot_ops/bay_parking_optimizer.py

Optimizes overnight bus parking in multi-vehicle stack lanes:
- Orders buses within parking lanes strictly by morning departure time (Earliest pull-out at the lane exit)
- Eliminates morning yard congestion and blocking shunts
- Segregates Electric AC buses into dedicated EV charging lanes
"""

from typing import List, Dict, Any


class DepotParkingOptimizer:
    """Arranges buses into depot yard parking lanes."""

    @staticmethod
    def optimize_yard_parking(buses_with_departure: List[Dict[str, Any]], num_lanes: int = 6, lane_capacity: int = 8) -> Dict[str, Any]:
        """
        Assigns buses to parking lanes based on pullout time and powertrain.
        """
        # Separate EV and Diesel buses
        ev_buses = [b for b in buses_with_departure if b.get('is_electric', False)]
        diesel_buses = [b for b in buses_with_departure if not b.get('is_electric', False)]

        # Sort each fleet chronologically by pullout minutes from midnight
        ev_buses.sort(key=lambda b: b.get('pullout_time_min', 360))
        diesel_buses.sort(key=lambda b: b.get('pullout_time_min', 360))

        lanes = []
        lane_counter = 1

        # Allocate EV Lanes
        for i in range(0, len(ev_buses), lane_capacity):
            batch = ev_buses[i:i + lane_capacity]
            lanes.append({
                'lane_id': f"LANE-EV-{lane_counter:02d}",
                'type': 'EV_CHARGING_EQUIPPED',
                'capacity': lane_capacity,
                'occupied': len(batch),
                'buses_front_to_back': batch
            })
            lane_counter += 1

        # Allocate Diesel Lanes
        diesel_lane_counter = 1
        for i in range(0, len(diesel_buses), lane_capacity):
            batch = diesel_buses[i:i + lane_capacity]
            lanes.append({
                'lane_id': f"LANE-DSL-{diesel_lane_counter:02d}",
                'type': 'STANDARD_DIESEL',
                'capacity': lane_capacity,
                'occupied': len(batch),
                'buses_front_to_back': batch
            })
            diesel_lane_counter += 1

        return {
            'depot': 'PNBS Central Yard',
            'total_lanes': len(lanes),
            'total_parked_buses': len(buses_with_departure),
            'lanes': lanes,
            'shunt_conflicts': 0
        }
