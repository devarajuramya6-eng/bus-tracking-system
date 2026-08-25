"""
CityBus Enterprise Platform - Bike Share Docking Station Inventory Rebalancer
File: backend/services/micromobility/docking_station_rebalancer.py

Optimizes bike fleet distribution across transit feeder docks:
- Identifies starved docks (0 bikes available for arriving bus passengers)
- Identifies full docks (100% capacity preventing drop-offs)
- Generates dynamic rebalancing truck route orders
"""

from typing import List, Dict, Any


class DockingStationRebalancer:
    @staticmethod
    def audit_dock_inventory(stations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates dock deficits and surpluses.
        """
        starved = []
        overflowing = []

        for s in stations:
            cap = s.get('capacity', 20)
            avail = s.get('available_bikes', 10)
            fill_pct = (avail / max(1, cap)) * 100.0

            if fill_pct <= 15.0: # Less than 15% bikes
                starved.append({'station_id': s.get('id'), 'name': s.get('name'), 'deficit_bikes': int(cap * 0.5 - avail)})
            elif fill_pct >= 85.0: # Over 85% full
                overflowing.append({'station_id': s.get('id'), 'name': s.get('name'), 'surplus_bikes': int(avail - cap * 0.5)})

        return {
            'total_stations_audited': len(stations),
            'starved_stations_count': len(starved),
            'overflowing_stations_count': len(overflowing),
            'starved_stations': starved,
            'overflowing_stations': overflowing,
            'rebalancing_truck_dispatch_recommended': len(starved) > 0 or len(overflowing) > 0
        }
