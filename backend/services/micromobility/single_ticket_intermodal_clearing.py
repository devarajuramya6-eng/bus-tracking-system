"""
CityBus Enterprise Platform - Unified Intermodal Bus + E-Bike Single Ticket Clearing
File: backend/services/micromobility/single_ticket_intermodal_clearing.py

Clears single-ticket intermodal journeys combining trunk bus + feeder e-bike:
- Combined booking with automatic ₹5 multimodal integration rebate
- Single QR code unlocks both bus validator gate and bike dock lock
"""

from typing import Dict, Any
from datetime import datetime


class IntermodalMicroTicketClearing:
    MULTIMODAL_DISCOUNT_INR = 5.0

    @staticmethod
    def create_intermodal_pass(user_id: int, bus_fare_inr: float, bike_duration_min: int, bike_rate_per_min: float = 1.0) -> Dict[str, Any]:
        """
        Generates single combined billing ticket for bus + e-bike trip.
        """
        bike_fare = bike_duration_min * bike_rate_per_min
        gross_total = bus_fare_inr + bike_fare
        net_payable = max(10.0, gross_total - IntermodalMicroTicketClearing.MULTIMODAL_DISCOUNT_INR)

        pass_id = f"INTERMODAL-{datetime.utcnow().strftime('%y%m%d%H%M')}-{user_id:03d}"

        return {
            'intermodal_ticket_id': pass_id,
            'user_id': user_id,
            'bus_leg_fare_inr': round(bus_fare_inr, 2),
            'bike_leg_minutes': bike_duration_min,
            'bike_leg_fare_inr': round(bike_fare, 2),
            'multimodal_transfer_discount_inr': IntermodalMicroTicketClearing.MULTIMODAL_DISCOUNT_INR,
            'total_amount_inr': round(net_payable, 2),
            'single_qr_unlock_code': f"QR-MULTI-{pass_id}",
            'status': 'BOOKED_ACTIVE'
        }
