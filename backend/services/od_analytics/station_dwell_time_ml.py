"""
CityBus Enterprise Platform - Machine Learning Station Dwell Time Predictor
File: backend/services/od_analytics/station_dwell_time_ml.py

Predicts bus stop passenger exchange dwell times (Highway Capacity Manual transit model):
- Door opening & closing dead time: 3.5 seconds
- Boarding time per passenger: 2.2s (Cash) vs 1.1s (Contactless Smart Card)
- Alighting time per passenger: 1.0s (Rear door)
- Wheelchair ramp deployment penalty: +45.0 seconds
"""

from typing import Dict, Any


class StationDwellTimePredictor:
    DEAD_TIME_SECONDS = 3.5
    BOARDING_TIME_CARD_SEC = 1.1
    BOARDING_TIME_CASH_SEC = 2.4
    ALIGHTING_TIME_SEC = 0.9
    WHEELCHAIR_RAMP_SEC = 45.0

    @staticmethod
    def predict_dwell_time(boardings_count: int, alightings_count: int,
                           smart_card_ratio: float = 0.65,
                           is_wheelchair_ramp_used: bool = False) -> Dict[str, Any]:
        """
        Estimates total stop dwell duration.
        """
        avg_board_sec = (smart_card_ratio * StationDwellTimePredictor.BOARDING_TIME_CARD_SEC) + \
                        ((1.0 - smart_card_ratio) * StationDwellTimePredictor.BOARDING_TIME_CASH_SEC)

        total_boarding_sec = boardings_count * avg_board_sec
        total_alighting_sec = alightings_count * StationDwellTimePredictor.ALIGHTING_TIME_SEC

        # Simultaneous 2-door operation: max of boarding (front) and alighting (rear)
        simultaneous_exchange_sec = max(total_boarding_sec, total_alighting_sec)
        ramp_time = StationDwellTimePredictor.WHEELCHAIR_RAMP_SEC if is_wheelchair_ramp_used else 0.0

        total_dwell_sec = StationDwellTimePredictor.DEAD_TIME_SECONDS + simultaneous_exchange_sec + ramp_time

        return {
            'boardings': boardings_count,
            'alightings': alightings_count,
            'smart_card_adoption_pct': round(smart_card_ratio * 100.0, 1),
            'wheelchair_ramp_deployed': is_wheelchair_ramp_used,
            'estimated_dwell_seconds': round(total_dwell_sec, 1),
            'dwell_classification': 'LONG_TERMINAL_DWELL' if total_dwell_sec > 45 else ('MEDIUM_STATION_STOP' if total_dwell_sec > 20 else 'QUICK_PASS_THROUGH')
        }
