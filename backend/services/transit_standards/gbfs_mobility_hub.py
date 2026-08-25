"""
CityBus Enterprise Platform - GBFS v2.2 Multi-Modal Mobility Hub Feed
File: backend/services/transit_standards/gbfs_mobility_hub.py

Publishes General Bikeshare Feed Specification (GBFS) data for first-mile/last-mile hubs:
- Station Information & Live Dock Availability
- Multi-modal feeder integration with CityBus terminals
"""

import time
from typing import Dict, Any, List


class GBFSMobilityHub:
    """Generates standard GBFS v2.2 JSON endpoints."""

    STATIONS = [
        {'station_id': 'HUB-PNBS-01', 'name': 'PNBS Central Smart Mobility Hub', 'lat': 16.5100, 'lon': 80.6175, 'capacity': 30, 'bikes_available': 18, 'docks_available': 12},
        {'station_id': 'HUB-BENZ-02', 'name': 'Benz Circle E-Bike Feeder Dock', 'lat': 16.5020, 'lon': 80.6475, 'capacity': 20, 'bikes_available': 11, 'docks_available': 9},
        {'station_id': 'HUB-RLWY-03', 'name': 'Vijayawada Junction Station Hub', 'lat': 16.5180, 'lon': 80.6200, 'capacity': 25, 'bikes_available': 14, 'docks_available': 11}
    ]

    @staticmethod
    def get_station_status() -> Dict[str, Any]:
        timestamp = int(time.time())
        stations_data = []

        for s in GBFSMobilityHub.STATIONS:
            stations_data.append({
                'station_id': s['station_id'],
                'num_bikes_available': s['bikes_available'],
                'num_docks_available': s['docks_available'],
                'is_installed': 1,
                'is_renting': 1,
                'is_returning': 1,
                'last_reported': timestamp
            })

        return {
            'last_updated': timestamp,
            'ttl': 60,
            'version': '2.2',
            'data': {
                'stations': stations_data
            }
        }
