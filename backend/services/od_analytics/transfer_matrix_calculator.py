"""
CityBus Enterprise Platform - Inter-Route Passenger Transfer Matrix Engine
File: backend/services/od_analytics/transfer_matrix_calculator.py

Analyzes multi-route commuter transfers at key transit exchange hubs:
- Identifies highest-volume intermodal transfer pairs (e.g. Route 27A ➔ Route 5K at PNBS)
- Calculates transfer penalty index and optimal synchronized departure banks
"""

from typing import List, Dict, Any


class TransferMatrixCalculator:
    @staticmethod
    def calculate_hub_transfers(smart_card_taps: List[Dict[str, Any]], max_transfer_window_sec: int = 2700) -> Dict[str, Any]:
        """
        Groups commuter tap-ins into multi-leg transfer journeys.
        """
        transfer_counts: Dict[str, int] = {}
        single_legs = 0
        transfer_legs = 0

        # Sort by user and timestamp
        sorted_taps = sorted(smart_card_taps, key=lambda t: (t.get('card_id', 0), t.get('timestamp_sec', 0)))

        for i in range(len(sorted_taps)):
            curr = sorted_taps[i]
            if i > 0:
                prev = sorted_taps[i-1]
                if prev.get('card_id') == curr.get('card_id'):
                    delta_t = curr.get('timestamp_sec', 0) - prev.get('timestamp_sec', 0)
                    if 0 < delta_t <= max_transfer_window_sec:
                        pair_key = f"{prev.get('route_num', '?')} ➔ {curr.get('route_num', '?')}"
                        transfer_counts[pair_key] = transfer_counts.get(pair_key, 0) + 1
                        transfer_legs += 1
                        continue
            single_legs += 1

        top_pairs = sorted([{'pair': k, 'count': v} for k, v in transfer_counts.items()], key=lambda x: x['count'], reverse=True)

        return {
            'total_trips_analyzed': len(smart_card_taps),
            'direct_single_trips': single_legs,
            'transfer_linked_trips': transfer_legs,
            'network_transfer_rate_pct': round((transfer_legs / max(1, len(smart_card_taps))) * 100.0, 1),
            'top_transfer_corridors': top_pairs[:5]
        }
