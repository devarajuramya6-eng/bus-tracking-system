"""
CityBus Enterprise Platform - Driver Destination LED Code Selector
File: backend/services/destination_led/route_code_lookup.py

Maps 3-digit driver console route codes (e.g. Code 127 = Route 27A PNBS ➔ Guntur) to Front, Side, and Rear LED signs:
- Front Board: Route Number + Destination Name (Alternating English / Telugu)
- Side Board: Route Number + Via Points
- Rear Board: Route Number only
"""

from typing import Dict, Any, List


class DestinationRouteCodeLookup:
    CODE_DATABASE = {
        127: {
            'route_number': '27A',
            'dest_en': 'GUNTUR BUS STATION',
            'dest_te': 'గుంటూరు బస్ స్టేషన్',
            'via_points': 'PNBS - Benz Circle - Mangalagiri AIIMS',
            'service_type': 'METRO_EXPRESS'
        },
        105: {
            'route_number': '5K',
            'dest_en': 'AUTONAGAR TERMINAL',
            'dest_te': 'ఆటోనగర్ టెర్మినల్',
            'via_points': 'Kaleswara Rao Market - Railway Station - Benz Circle',
            'service_type': 'CITY_ORDINARY'
        },
        100: {
            'route_number': '100E',
            'dest_en': 'GANNAVARAM AIRPORT',
            'dest_te': 'గన్నవరం విమానాశ్రయం',
            'via_points': 'PNBS - Ramavarappadu - Enikepadu',
            'service_type': 'ELECTRIC_AC'
        }
    }

    @staticmethod
    def lookup_route_code(code: int) -> Dict[str, Any]:
        """
        Retrieves destination sign payloads for front/side/rear signs.
        """
        data = DestinationRouteCodeLookup.CODE_DATABASE.get(code)
        if not data:
            return {
                'code': code,
                'front_sign_en': 'SPECIAL SERVICE',
                'front_sign_te': 'ప్రత్యేక సేవ',
                'status': 'DEFAULT_FALLBACK'
            }

        return {
            'code': code,
            'front_sign': f"{data['route_number']} {data['dest_en']}",
            'front_sign_te': f"{data['route_number']} {data['dest_te']}",
            'side_sign': f"{data['route_number']} VIA {data['via_points']}",
            'rear_sign': data['route_number'],
            'service_type': data['service_type'],
            'status': 'CODE_FOUND'
        }
