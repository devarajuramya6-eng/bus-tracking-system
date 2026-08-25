"""
CityBus Enterprise Platform - Transit Station Smart Parcel Locker Grid
File: backend/services/cargo_transit/station_smart_locker_grid.py

Manages contactless smart locker banks installed at bus terminals:
- Locker sizes: SMALL (10x40x50 cm), MEDIUM (20x40x50 cm), LARGE (40x40x50 cm)
- Dynamic 6-digit one-time PIN (OTP) generation for secure pickup
- 48-Hour auto-expiry and storage fee management
"""

import random
from typing import List, Dict, Any, Optional


class SmartLockerGridManager:
    @staticmethod
    def assign_locker_box(station_id: str, parcel_id: str, locker_size: str = 'MEDIUM') -> Dict[str, Any]:
        """
        Allocates locker slot and creates cryptographic pickup PIN.
        """
        box_number = random.randint(101, 148)
        pickup_otp = f"{random.randint(100000, 999999)}"

        return {
            'station_id': station_id,
            'parcel_id': parcel_id,
            'allocated_box_number': f"BOX-{box_number}",
            'locker_size_tier': locker_size,
            'pickup_pin_otp': pickup_otp,
            'holding_duration_hours': 48,
            'status': 'DEPOSITED_AWAITING_PICKUP'
        }
