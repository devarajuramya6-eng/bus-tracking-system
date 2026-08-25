"""
CityBus Enterprise Platform - GTFS-Realtime TripUpdates Feed Builder
File: backend/services/open_data/gtfs_realtime_trip_updates.py

Serializes standard GTFS-RT TripUpdate feed objects (Google Transit / MobilityData spec):
- stop_time_update with arrival / departure delay seconds
- schedule_relationship: SCHEDULED, ADDED, UNSCHEDULED, CANCELED
"""

import time
from typing import List, Dict, Any


class GTFSTripUpdatesFeed:
    @staticmethod
    def build_feed(trip_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds standard GTFS-RT FeedMessage structure.
        """
        entities = []
        now_ts = int(time.time())

        for idx, tu in enumerate(trip_updates):
            stop_time_updates = []
            for stu in tu.get('stops', []):
                stop_time_updates.append({
                    'stop_sequence': stu.get('stop_sequence', 1),
                    'stop_id': str(stu.get('stop_id', '')),
                    'arrival': {
                        'delay': stu.get('delay_seconds', 0),
                        'time': now_ts + stu.get('delay_seconds', 0)
                    },
                    'departure': {
                        'delay': stu.get('delay_seconds', 0),
                        'time': now_ts + stu.get('delay_seconds', 0) + 30
                    },
                    'schedule_relationship': 'SCHEDULED'
                })

            entities.append({
                'id': f"TU_{tu.get('trip_id', idx)}",
                'trip_update': {
                    'trip': {
                        'trip_id': str(tu.get('trip_id', '')),
                        'route_id': str(tu.get('route_id', '')),
                        'start_time': tu.get('start_time', '06:00:00'),
                        'start_date': tu.get('start_date', '20260825'),
                        'schedule_relationship': 'SCHEDULED'
                    },
                    'vehicle': {
                        'id': str(tu.get('vehicle_id', '')),
                        'label': tu.get('vehicle_label', '')
                    },
                    'stop_time_update': stop_time_updates,
                    'timestamp': now_ts
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
