"""
CityBus Enterprise Platform - Multi-Zone & Distance-Tiered Fare Matrix Engine
File: backend/services/fare/multi_zone_matrix.py

Computes zonal and distance-tiered transit fares:
- Zone 1: Vijayawada Core (PNBS, Benz Circle, Railway Station, Bhavanipuram)
- Zone 2: Suburbs & Mangalagiri AIIMS
- Zone 3: Amaravati Capital Core & Secretariat
- Zone 4: Regional Transit (Gannavaram Airport & Guntur)
- Concession rules: Student (50%), Senior (30%), Differently Abled (100% Free)
"""

from typing import Dict, Any, Optional


class MultiZoneFareMatrix:
    ZONES = {
        'ZONE_1_CORE': {'name': 'Vijayawada Core Metro', 'base_rate': 15.0},
        'ZONE_2_SUBURB': {'name': 'Mangalagiri & Suburbs', 'base_rate': 25.0},
        'ZONE_3_CAPITAL': {'name': 'Amaravati Capital Region', 'base_rate': 35.0},
        'ZONE_4_REGIONAL': {'name': 'Airport & Guntur Corridors', 'base_rate': 45.0}
    }

    CONCESSION_DISCOUNTS = {
        'general': 0.0,
        'student': 0.50, # 50% off
        'senior': 0.30,  # 30% off
        'divyang': 1.00, # 100% free pass
        'journalist': 0.50
    }

    @staticmethod
    def calculate_fare(origin_zone: str, dest_zone: str,
                       distance_km: float,
                       concession_type: str = 'general',
                       passenger_count: int = 1,
                       is_peak_hour: bool = False) -> Dict[str, Any]:
        """
        Calculates exact trip fare with zone crossing rules and concessions.
        """
        base_origin = MultiZoneFareMatrix.ZONES.get(origin_zone, {}).get('base_rate', 15.0)
        base_dest = MultiZoneFareMatrix.ZONES.get(dest_zone, {}).get('base_rate', 15.0)

        # Baseline distance rate (Rs 1.40 per km)
        distance_charge = distance_km * 1.40
        base_fare = max(base_origin, base_dest) + distance_charge

        # Peak hour surcharge (+10% during heavy demand to balance loading)
        if is_peak_hour:
            base_fare *= 1.10

        discount_pct = MultiZoneFareMatrix.CONCESSION_DISCOUNTS.get(concession_type.lower(), 0.0)
        unit_fare = round(base_fare * (1.0 - discount_pct), 2)
        total_fare = round(unit_fare * passenger_count, 2)

        return {
            'origin_zone': origin_zone,
            'destination_zone': dest_zone,
            'distance_km': round(distance_km, 2),
            'concession_type': concession_type,
            'discount_percentage': int(discount_pct * 100),
            'is_peak_hour': is_peak_hour,
            'unit_fare': unit_fare,
            'passenger_count': passenger_count,
            'total_fare': total_fare,
            'currency': 'INR'
        }
