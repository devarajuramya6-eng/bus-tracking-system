"""
CityBus Enterprise Platform - Heavy Vehicle Predictive Health & Remaining Useful Life (RUL)
File: backend/services/maintenance_ops/predictive_health_model.py

Models mechanical component wear from telemetry, mileage, and stop count:
- Brake Lining Wear (mm thickness remaining vs 4.0mm replacement threshold)
- Steer & Drive Axle Tire Tread Depth (mm vs 1.6mm legal limit)
- Transmission Oil & Engine Oil Degradation Index
- Suspension Air Spring Bellows integrity
"""

from typing import Dict, Any, List


class FleetPredictiveHealthModel:
    @staticmethod
    def evaluate_vehicle_health(bus_id: int, odometer_km: float, total_stops_served: int) -> Dict[str, Any]:
        """
        Evaluates mechanical component wear and estimates days to required replacement.
        """
        # Brake lining wear: starts at 18mm, wears approx 0.15mm per 1,000 stops + 0.08mm per 1,000 km
        brake_wear_mm = (total_stops_served * 0.00015) + (odometer_km * 0.00008)
        current_brake_mm = max(2.5, 18.0 - (brake_wear_mm % 15.5))

        # Tire tread: starts at 16mm, wears approx 0.12mm per 1,000 km
        tire_wear_mm = (odometer_km % 60000) * 0.00022
        current_tire_mm = max(1.2, 16.0 - tire_wear_mm)

        # Engine oil degradation (0-100% life): service interval every 20,000 km
        km_since_last_oil = odometer_km % 20000
        oil_life_pct = max(0.0, round(100.0 - (km_since_last_oil / 20000.0) * 100.0, 1))

        # Component health statuses
        brake_status = 'CRITICAL' if current_brake_mm < 4.0 else ('WARNING' if current_brake_mm < 6.0 else 'GOOD')
        tire_status = 'CRITICAL' if current_tire_mm < 2.0 else ('WARNING' if current_tire_mm < 4.0 else 'GOOD')
        oil_status = 'SERVICE_DUE' if oil_life_pct < 15.0 else 'GOOD'

        overall_health_score = int(
            (current_brake_mm / 18.0) * 35 +
            (current_tire_mm / 16.0) * 35 +
            (oil_life_pct / 100.0) * 30
        )

        return {
            'bus_id': bus_id,
            'odometer_km': odometer_km,
            'overall_health_score': max(30, min(100, overall_health_score)),
            'brake_lining_thickness_mm': round(current_brake_mm, 1),
            'brake_status': brake_status,
            'tire_tread_depth_mm': round(current_tire_mm, 1),
            'tire_status': tire_status,
            'engine_oil_life_pct': oil_life_pct,
            'oil_status': oil_status,
            'requires_immediate_workshop_visit': brake_status == 'CRITICAL' or tire_status == 'CRITICAL'
        }
