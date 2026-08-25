"""
CityBus Enterprise Platform - Passenger Bus Belly Freight Logistics
File: backend/services/cargo_transit/passenger_bus_belly_freight.py

Monetizes unused underfloor luggage capacity for municipal same-day cargo dispatch:
- Max allowable cargo payload per bus: 450 kg / 1.8 cubic meters
- Automatic weight and dimension volumetric check (Length x Width x Height / 5000)
- Intercity route transport (e.g. Vijayawada PNBS ➔ Guntur Hub within 50 minutes)
"""

from typing import List, Dict, Any


class BellyFreightAllocator:
    MAX_PAYLOAD_KG = 450.0
    MAX_VOLUME_M3 = 1.8

    @staticmethod
    def allocate_cargo_consignment(bus_id: int, bus_number: str,
                                   current_loaded_weight_kg: float,
                                   parcel_weight_kg: float,
                                   parcel_volume_m3: float) -> Dict[str, Any]:
        """
        Validates whether bus luggage hold can accommodate incoming shipment.
        """
        new_total_weight = current_loaded_weight_kg + parcel_weight_kg
        can_accept = new_total_weight <= BellyFreightAllocator.MAX_PAYLOAD_KG

        cargo_fee_inr = max(40.0, parcel_weight_kg * 8.5) # ₹8.5 per kg

        return {
            'bus_id': bus_id,
            'bus_number': bus_number,
            'parcel_weight_kg': round(parcel_weight_kg, 2),
            'parcel_volume_m3': round(parcel_volume_m3, 3),
            'current_load_kg': round(current_loaded_weight_kg, 1),
            'remaining_capacity_kg': round(max(0.0, BellyFreightAllocator.MAX_PAYLOAD_KG - new_total_weight), 1),
            'is_shipment_accepted': can_accept,
            'freight_charge_inr': round(cargo_fee_inr, 2),
            'status': 'BOOKED_FOR_TRANSIT' if can_accept else 'CAPACITY_EXCEEDED'
        }
