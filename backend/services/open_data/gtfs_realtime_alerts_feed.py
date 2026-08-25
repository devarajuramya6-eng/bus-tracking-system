"""
CityBus Enterprise Platform - GTFS-Realtime Service Alerts Feed Builder
File: backend/services/open_data/gtfs_realtime_alerts_feed.py

Serializes standard GTFS-RT Service Alert feed entities:
- Informed entities: route_id, stop_id, agency_id
- Translated header text, description text, and URL
- Cause and Effect categorization (WEATHER, CONSTRUCTION, ACCIDENT, DETOUR, MODIFIED_SERVICE)
"""

import time
from typing import List, Dict, Any


class GTFSServiceAlertsFeed:
    @staticmethod
    def build_feed(alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds standard GTFS-RT ServiceAlerts FeedMessage structure.
        """
        entities = []
        now_ts = int(time.time())

        for idx, alt in enumerate(alerts):
            entities.append({
                'id': f"ALERT_{alt.get('id', idx+1)}",
                'alert': {
                    'active_period': [{
                        'start': alt.get('start_time', now_ts),
                        'end': alt.get('end_time', now_ts + 86400)
                    }],
                    'informed_entity': [{
                        'route_id': str(alt.get('route_id', '27A')),
                        'agency_id': 'APSRTC_VIJAYAWADA'
                    }],
                    'cause': alt.get('cause', 'WEATHER'),
                    'effect': alt.get('effect', 'DETOUR'),
                    'header_text': {
                        'translation': [
                            {'text': alt.get('title_en', ''), 'language': 'en'},
                            {'text': alt.get('title_te', alt.get('title_en', '')), 'language': 'te'}
                        ]
                    },
                    'description_text': {
                        'translation': [
                            {'text': alt.get('desc_en', ''), 'language': 'en'},
                            {'text': alt.get('desc_te', alt.get('desc_en', '')), 'language': 'te'}
                        ]
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
