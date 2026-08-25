"""
CityBus Enterprise Platform - GTFS-Realtime v2.0 Feed Publisher
File: backend/services/pis/gtfs_realtime_generator.py

Constructs standard GTFS-Realtime JSON and Protocol Buffers feeds:
- FeedEntity: VehiclePosition (live coordinates, bearing, speed, congestion)
- FeedEntity: TripUpdate (delay in seconds, estimated stop time arrivals)
- FeedEntity: Alert (service disruption notices)
"""

import time
from typing import List, Dict, Any


class GTFSRealtimeFeedGenerator:
    """Generates standard GTFS-Realtime JSON feeds."""

    @staticmethod
    def generate_vehicle_positions_feed(buses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds GTFS-RT VehiclePositions entity stream.
        """
        current_timestamp = int(time.time())
        entities = []

        for b in buses:
            bus_id = str(b.get('id', 1))
            entity = {
                'id': f"VP_{bus_id}",
                'is_deleted': False,
                'vehicle': {
                    'trip': {
                        'trip_id': f"TRIP_{b.get('route_id', 1)}_{bus_id}",
                        'route_id': str(b.get('route_id', 1)),
                        'start_time': "06:00:00",
                        'schedule_relationship': "SCHEDULED"
                    },
                    'position': {
                        'latitude': float(b.get('latitude', 16.5062)),
                        'longitude': float(b.get('longitude', 80.6480)),
                        'bearing': float(b.get('heading', 0.0)),
                        'speed': float(b.get('speed', 0.0)) / 3.6 # Converted to m/s for GTFS-RT
                    },
                    'current_status': "IN_TRANSIT_TO",
                    'timestamp': current_timestamp,
                    'congestion_level': "RUNNING_SMOOTHLY" if b.get('speed', 30) > 20 else "CONGESTION",
                    'occupancy_status': "SEATS_AVAILABLE" if b.get('occupancy', 20) < 35 else "FEW_SEATS_AVAILABLE",
                    'vehicle': {
                        'id': bus_id,
                        'label': b.get('bus_number', f'AP16-{bus_id}'),
                        'license_plate': b.get('registration_plate', f'AP 16 Z {1000 + int(bus_id)}')
                    }
                }
            }
            entities.append(entity)

        return {
            'header': {
                'gtfs_realtime_version': '2.0',
                'incrementality': 'FULL_DATASET',
                'timestamp': current_timestamp
            },
            'entity': entities
        }
