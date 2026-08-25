"""
CityBus Enterprise Platform - GTFS-Realtime VehiclePositions Feed Builder
File: backend/services/open_data/gtfs_realtime_vehicle_feed.py

Serializes standard GTFS-RT VehiclePosition entities:
- Position (latitude, longitude, bearing, speed m/s)
- Current status: INCOMING_AT, STOPPED_AT, IN_TRANSIT_TO
- Occupancy status: MANY_SEATS_AVAILABLE, FEW_SEATS_AVAILABLE, STANDING_ROOM_ONLY, FULL
"""

import time
from typing import List, Dict, Any


class GTFSVehiclePositionsFeed:
    @staticmethod
    def build_feed(vehicles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds standard GTFS-RT VehiclePositions FeedMessage structure.
        """
        entities = []
        now_ts = int(time.time())

        for v in vehicles:
            pax = v.get('occupancy', 20)
            if pax > 40:
                occ_status = 'STANDING_ROOM_ONLY'
            elif pax > 25:
                occ_status = 'FEW_SEATS_AVAILABLE'
            else:
                occ_status = 'MANY_SEATS_AVAILABLE'

            speed_mps = (v.get('speed', 30.0) * 1000.0) / 3600.0

            entities.append({
                'id': f"VP_{v.get('id', 1)}",
                'vehicle': {
                    'trip': {
                        'trip_id': str(v.get('trip_id', f"TRIP_{v.get('id', 1)}")),
                        'route_id': str(v.get('route_id', '1'))
                    },
                    'position': {
                        'latitude': float(v.get('latitude', 16.5062)),
                        'longitude': float(v.get('longitude', 80.6480)),
                        'bearing': float(v.get('heading', 90.0)),
                        'speed': round(speed_mps, 2)
                    },
                    'current_stop_sequence': v.get('stop_sequence', 1),
                    'current_status': 'IN_TRANSIT_TO' if v.get('speed', 0) > 5 else 'STOPPED_AT',
                    'timestamp': now_ts,
                    'congestion_level': 'RUNNING_SMOOTHLY',
                    'occupancy_status': occ_status,
                    'vehicle': {
                        'id': str(v.get('id', 1)),
                        'label': v.get('bus_number', 'AP16-001')
                    }
                }
            })

        return {
            'header': {
                'gtfs_realtime_version': '2.0',
                'incrementality': 'FULL_DATASET',
                'timestamp': now_ts
            },
            'entity': entities
        }
