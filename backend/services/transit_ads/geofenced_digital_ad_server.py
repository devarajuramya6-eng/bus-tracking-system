"""
CityBus Enterprise Platform - GPS Geofenced In-Bus Digital Ad Server
File: backend/services/transit_ads/geofenced_digital_ad_server.py

Delivers location-targeted commercial ads on in-cabin 29-inch ultra-wide screens:
- GPS Geofenced Campaigns (e.g. Trendset Mall discount QR codes when approaching Benz Circle)
- Day-parting scheduling (Morning: Breakfast cafes / Evening: Retail & Entertainment)
- CPM (Cost-per-thousand) programmatic revenue generation for municipal transit authority
"""

from typing import List, Dict, Any


class GeofencedAdServer:
    ACTIVE_CAMPAIGNS = [
        {
            'campaign_id': 'CAMP_MALL_01',
            'sponsor': 'Trendset Mall Vijayawada',
            'target_lat': 16.5062,
            'target_lng': 80.6480,
            'radius_m': 600,
            'creative_url': 'https://citybus.vijayawada.gov.in/ads/trendset_winter_sale.mp4',
            'ad_title': 'Trendset Mall: 50% Off Mega Sale',
            'cpm_rate_inr': 180.0
        },
        {
            'campaign_id': 'CAMP_AIIMS_02',
            'sponsor': 'Mangalagiri AIIMS Health Checkup',
            'target_lat': 16.4420,
            'target_lng': 80.5780,
            'radius_m': 1000,
            'creative_url': 'https://citybus.vijayawada.gov.in/ads/aiims_health_check.mp4',
            'ad_title': 'AIIMS Mangalagiri: Comprehensive Health Screening',
            'cpm_rate_inr': 150.0
        }
    ]

    @staticmethod
    def get_ad_for_location(current_lat: float, current_lng: float) -> Dict[str, Any]:
        """
        Retrieves matching geofenced campaign.
        """
        for camp in GeofencedAdServer.ACTIVE_CAMPAIGNS:
            d_lat = current_lat - camp['target_lat']
            d_lng = current_lng - camp['target_lng']
            dist_m = ((d_lat*d_lat + d_lng*d_lng) ** 0.5) * 111000.0

            if dist_m <= camp['radius_m']:
                return {
                    'campaign_id': camp['campaign_id'],
                    'sponsor': camp['sponsor'],
                    'ad_title': camp['ad_title'],
                    'creative_media_url': camp['creative_url'],
                    'is_geofenced_match': True,
                    'status': 'SERVE_GEOFENCED_CAMPAIGN'
                }

        return {
            'campaign_id': 'CAMP_DEFAULT_CIVIC',
            'sponsor': 'Vijayawada Municipal Corporation',
            'ad_title': 'Keep Vijayawada Clean & Green (Swachh Survekshan)',
            'creative_media_url': 'https://citybus.vijayawada.gov.in/ads/swachh_vijayawada.mp4',
            'is_geofenced_match': False,
            'status': 'SERVE_DEFAULT_CIVIC_CAMPAIGN'
        }
