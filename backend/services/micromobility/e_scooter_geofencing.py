"""
CityBus Enterprise Platform - Shared Micro-Mobility Geofence & Speed Governor
File: backend/services/micromobility/e_scooter_geofencing.py

Enforces municipal geofences on shared electric feeder bikes and scooters:
- NO_RIDE_ZONE: Motor throttle completely disabled (Temples, pedestrian walkways)
- LOW_SPEED_ZONE: Maximum speed governed to 10 km/h (Bus terminal concourses)
- NORMAL_ZONE: Standard 25 km/h urban speed limit
"""

from typing import Dict, Any, List


class MicroMobilityGeofenceEngine:
    GEOFENCES = [
        {'id': 'GF_TEMPLE_STEPS', 'name': 'Indrakeeladri Temple Pedestrian Steps', 'lat': 16.5140, 'lng': 80.6050, 'radius_m': 400, 'rule': 'NO_RIDE_ZONE'},
        {'id': 'GF_PNBS_TERMINAL', 'name': 'PNBS Bus Bay Concourse', 'lat': 16.5100, 'lng': 80.6175, 'radius_m': 300, 'rule': 'LOW_SPEED_ZONE'}
    ]

    @staticmethod
    def evaluate_vehicle_position(lat: float, lng: float, current_speed_kmh: float) -> Dict[str, Any]:
        """
        Evaluates geofence rule and enforces electronic throttle limit.
        """
        for gf in MicroMobilityGeofenceEngine.GEOFENCES:
            d_lat = lat - gf['lat']
            d_lng = lng - gf['lng']
            dist_m = (d_lat*d_lat + d_lng*d_lng) ** 0.5 * 111000.0

            if dist_m <= gf['radius_m']:
                if gf['rule'] == 'NO_RIDE_ZONE':
                    return {
                        'geofence_id': gf['id'],
                        'zone_name': gf['name'],
                        'active_rule': 'NO_RIDE_ZONE',
                        'motor_throttle_enabled': False,
                        'max_allowable_speed_kmh': 0.0,
                        'warning_message': f"Entering {gf['name']}. Riding prohibited. Please walk your bike."
                    }
                elif gf['rule'] == 'LOW_SPEED_ZONE':
                    return {
                        'geofence_id': gf['id'],
                        'zone_name': gf['name'],
                        'active_rule': 'LOW_SPEED_ZONE',
                        'motor_throttle_enabled': True,
                        'max_allowable_speed_kmh': 10.0,
                        'warning_message': f"Slow speed zone ({gf['name']}). Speed capped at 10 km/h."
                    }

        return {
            'geofence_id': 'MUNICIPAL_STANDARD',
            'zone_name': 'Vijayawada Open Street Corridor',
            'active_rule': 'STANDARD_RIDE_ZONE',
            'motor_throttle_enabled': True,
            'max_allowable_speed_kmh': 25.0,
            'warning_message': 'Safe riding. Wear a helmet.'
        }
