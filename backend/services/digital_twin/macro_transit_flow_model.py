"""
CityBus Enterprise Platform - Macroscopic Fundamental Diagram (MFD) Flow Model
File: backend/services/digital_twin/macro_transit_flow_model.py

Models macroscopic urban network traffic flow and congestion dynamics:
- Density vs Speed relationship: Greenshields / Newell parabolic speed-density curve
- Identifies network critical density ($k_{crit}$) beyond which gridlock occurs
- Predicts average network bus travel speeds under varying private vehicle congestion levels
"""

from typing import Dict, Any


class MacroscopicFlowModel:
    FREE_FLOW_SPEED_KMH = 50.0
    JAM_DENSITY_VEH_PER_KM = 120.0
    CRITICAL_DENSITY_VEH_PER_KM = 45.0

    @staticmethod
    def evaluate_corridor_flow(current_density_veh_km: float) -> Dict[str, Any]:
        """
        Calculates space-mean speed and traffic flow state.
        """
        k = min(MacroscopicFlowModel.JAM_DENSITY_VEH_PER_KM, max(0.0, current_density_veh_km))

        # Greenshields model: v(k) = v_f * (1 - k / k_jam)
        speed_kmh = MacroscopicFlowModel.FREE_FLOW_SPEED_KMH * (1.0 - (k / MacroscopicFlowModel.JAM_DENSITY_VEH_PER_KM))
        speed_kmh = max(5.0, speed_kmh)

        # Flow q = k * v (veh/hr)
        flow_q = k * speed_kmh

        is_congested = k > MacroscopicFlowModel.CRITICAL_DENSITY_VEH_PER_KM

        return {
            'density_veh_per_km': round(k, 1),
            'space_mean_speed_kmh': round(speed_kmh, 1),
            'flow_rate_veh_per_hour': round(flow_q, 1),
            'critical_density_threshold': MacroscopicFlowModel.CRITICAL_DENSITY_VEH_PER_KM,
            'is_in_hyper_congestion': is_congested,
            'service_level': 'LOS_F_GRIDLOCK' if speed_kmh < 15.0 else ('LOS_D_CONGESTED' if is_congested else 'LOS_B_FREE_FLOW')
        }
