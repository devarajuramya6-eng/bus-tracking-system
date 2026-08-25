"""
CityBus Enterprise Platform - SAE J1939 Commercial CAN-Bus Decoder
File: backend/services/j1939_telematics/pgn_spn_multiplexer.py

Decodes SAE J1939 29-bit CAN identifiers and 8-byte payload frames:
- PGN 61444 (EEC1): Engine Speed (SPN 190, 0.125 rpm/bit), Engine Demand Torque (SPN 512)
- PGN 65262 (ET1): Engine Coolant Temp (SPN 110, -40°C offset), Engine Oil Temp (SPN 175)
- PGN 65265 (CCVS): Wheel-Based Vehicle Speed (SPN 84, 1/256 km/h per bit)
"""

from typing import Dict, Any


class J1939PGNSPNDecoder:
    @staticmethod
    def decode_eec1_frame(can_id: int, payload_bytes: bytes) -> Dict[str, Any]:
        """
        Decodes PGN 61444 (0xF004) Electronic Engine Controller 1.
        """
        if len(payload_bytes) < 8:
            return {'status': 'INVALID_PAYLOAD_LENGTH'}

        # SPN 190 Engine Speed (Bytes 4 and 5, little-endian, resolution 0.125 rpm/bit)
        raw_rpm = payload_bytes[3] | (payload_bytes[4] << 8)
        engine_rpm = raw_rpm * 0.125

        # SPN 513 Actual Engine Percent Torque (Byte 3, offset -125%)
        actual_torque_pct = payload_bytes[2] - 125

        # SPN 898 Engine Requested Speed Control Conditions (Byte 1)
        driver_demand_torque_pct = payload_bytes[1] - 125

        return {
            'pgn': 61444,
            'pgn_hex': '0xF004',
            'engine_speed_rpm': round(engine_rpm, 1),
            'actual_engine_torque_pct': actual_torque_pct,
            'driver_demand_torque_pct': driver_demand_torque_pct,
            'is_engine_overspeed': engine_rpm > 2400.0,
            'status': 'DECODED_SUCCESS'
        }
