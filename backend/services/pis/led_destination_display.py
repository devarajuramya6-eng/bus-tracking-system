"""
CityBus Enterprise Platform - Bilingual Electronic LED Destination Board Signage
File: backend/services/pis/led_destination_display.py

Generates formatted character matrices and display payloads for bus destination LED signboards:
- Front Header Display (Route Number + Telugu Destination / English Destination flip)
- Side Route Board (Key intermediate via stops)
- Interior Saloon Next-Stop LED Display
"""

from typing import Dict, Any, List


class LEDDestinationDisplay:
    ROUTE_SIGNAGE_MAP = {
        '27A': {
            'telugu_dest': 'గుంటూరు బస్ స్టేషన్',
            'english_dest': 'GUNTUR BUS STATION',
            'via_stops': 'VIA: BENZ CIRCLE, MANGALAGIRI, TADEPALLI',
            'badge_color': '#EF4444'
        },
        '5K': {
            'telugu_dest': 'ఆటోనగర్ బస్ డిపో',
            'english_dest': 'AUTONAGAR DEPOT',
            'via_stops': 'VIA: GOVT HOSPITAL, BENZ CIRCLE, PATAMATA',
            'badge_color': '#3B82F6'
        },
        '10': {
            'telugu_dest': 'గన్నవరం విమానాశ్రయం',
            'english_dest': 'GANNAVARAM AIRPORT',
            'via_stops': 'VIA: RAMAVARAPPADU RING, ENIKEPADU, PRASADAMPADU',
            'badge_color': '#10B981'
        },
        '222': {
            'telugu_dest': 'అమరావతి సెక్రటేరియట్',
            'english_dest': 'AMARAVATI SECRETARIAT',
            'via_stops': 'VIA: PRAKASAM BARRAGE, UNDAVALLI, VELAGAPUDI',
            'badge_color': '#8B5CF6'
        }
    }

    @staticmethod
    def get_display_payload(route_number: str, next_stop_name: str = "") -> Dict[str, Any]:
        """
        Builds digital signage payload for bus destination boards.
        """
        clean_num = route_number.upper().strip()
        info = LEDDestinationDisplay.ROUTE_SIGNAGE_MAP.get(clean_num, {
            'telugu_dest': 'సిటీ బస్సు సర్వీస్',
            'english_dest': 'CITYBUS METRO SERVICE',
            'via_stops': 'VIA: METROPOLITAN CORRIDOR',
            'badge_color': '#2563EB'
        })

        return {
            'route_number': clean_num,
            'front_display': {
                'line_1_telugu': info['telugu_dest'],
                'line_1_english': info['english_dest'],
                'line_2_via': info['via_stops'],
                'flip_interval_sec': 4
            },
            'side_display': {
                'route': clean_num,
                'destination': info['english_dest'],
                'via': info['via_stops']
            },
            'saloon_interior_display': {
                'next_stop': next_stop_name or "Approaching Next Terminal",
                'message': f"Route {clean_num} ➔ Next: {next_stop_name}" if next_stop_name else f"Route {clean_num}"
            }
        }
