"""
CityBus Enterprise Platform - 4K Hub Departure Board Multi-Screen Renderer
File: backend/services/hub_signage/multi_screen_split_renderer.py

Compiles 4K high-density departure board layouts for terminal digital displays:
- Next 10 scheduled departures with live ETA countdown (Minutes remaining)
- Real-time service status (ON_TIME, DELAYED_5M, BOARDING, DEPARTED)
- Bilingual Telugu and English destination ticker
"""

from typing import List, Dict, Any


class MultiScreenDepartureRenderer:
    @staticmethod
    def render_departure_board_json(departures: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds digital signage layout payload.
        """
        rows = []
        for d in departures[:10]:
            eta = d.get('eta_minutes', 5)
            if eta <= 1:
                status_text = 'BOARDING NOW'
                badge_color = '#10B981' # Green
            elif eta > 10:
                status_text = f"{eta} MINS"
                badge_color = '#38BDF8' # Blue
            else:
                status_text = f"{eta} MINS"
                badge_color = '#F59E0B' # Amber

            rows.append({
                'route': d.get('route_number'),
                'destination_en': d.get('destination_en'),
                'destination_te': d.get('destination_te'),
                'platform_bay': d.get('bay', 'BAY_01'),
                'service_type': d.get('type', 'EXPRESS'),
                'eta_minutes': eta,
                'status_label': status_text,
                'status_color': badge_color
            })

        return {
            'display_terminal_id': 'PNBS_MAIN_CONCOURSE_4K_01',
            'screen_refresh_interval_sec': 5,
            'total_departures_listed': len(rows),
            'departures': rows
        }
