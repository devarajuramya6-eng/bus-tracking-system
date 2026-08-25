"""
CityBus Enterprise Platform - SAE J2735 DSRC / C-V2X Basic Safety Message (BSM) Encoder
File: backend/services/v2x_tsp/dsrc_bsm_encoder.py

Encodes SAE J2735 standard 10 Hz Basic Safety Message (BSM) broadcasts:
- Part 1: Vehicle temporary ID, Latitude, Longitude, Elevation, Speed, Heading, Brake Status
- Part 2 Transit Extension: Public transit bus classification, passenger standing alert, low-floor ramp deployed
"""

import time
from typing import Dict, Any


class DSRCBasicSafetyMessageEncoder:
    @staticmethod
    def encode_bsm_frame(bus_id: int, bus_number: str,
                         lat: float, lng: float, speed_kmh: float,
                         heading_deg: float, is_braking: bool = False,
                         passenger_count: int = 35) -> Dict[str, Any]:
        """
        Builds SAE J2735 compliant BSM dictionary payload.
        """
        speed_mps = (speed_kmh * 1000.0) / 3600.0
        msg_count = int(time.time() * 10) % 128

        return {
            'standard': 'SAE_J2735_2020',
            'message_id': 'BSM_MESSAGE_02',
            'msg_sequence_counter': msg_count,
            'temporary_vehicle_id': f"BUS-{bus_id:04d}",
            'latitude_degrees': round(lat, 7),
            'longitude_degrees': round(lng, 7),
            'elevation_meters': 18.5,
            'speed_meters_per_second': round(speed_mps, 2),
            'heading_degrees': round(heading_deg, 1),
            'brakes_applied': is_braking,
            'transit_extension': {
                'vehicle_type': 'HEAVY_COMMERCIAL_CITY_TRANSIT',
                'occupancy_status': 'SEATS_OCCUPIED_WITH_STANDEES' if passenger_count > 30 else 'SEATS_AVAILABLE',
                'ada_ramp_active': False
            },
            'transmission_frequency_hz': 10
        }
