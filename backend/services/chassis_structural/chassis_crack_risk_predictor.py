"""
CityBus Enterprise Platform - Weibull Chassis Crack Initiation Risk Model
File: backend/services/chassis_structural/chassis_crack_risk_predictor.py

Predicts weld crack initiation probability using 2-parameter Weibull model:
- Shape Parameter $\beta = 2.8$ (Wear-out / metal fatigue aging phase)
- Characteristic Life $\eta = 750,000\text{ km}$
- Triggers Magnetic Particle (MPI) or Ultrasonic Non-Destructive Testing (NDT) if probability > 15%
"""

import math
from typing import Dict, Any


class ChassisCrackPredictor:
    BETA_SHAPE = 2.8
    ETA_SCALE_KM = 750000.0

    @staticmethod
    def predict_crack_risk(accumulated_odometer_km: float,
                           rough_road_severity_factor: float = 1.0) -> Dict[str, Any]:
        """
        Computes cumulative failure probability $F(t) = 1 - \exp(-(t/\eta)^\beta)$.
        """
        effective_km = accumulated_odometer_km * rough_road_severity_factor
        t_over_eta = effective_km / ChassisCrackPredictor.ETA_SCALE_KM
        
        # Weibull CDF
        cum_prob = 1.0 - math.exp(-(t_over_eta ** ChassisCrackPredictor.BETA_SHAPE))
        prob_pct = cum_prob * 100.0

        is_mpi_inspection_required = prob_pct >= 15.0

        return {
            'odometer_km': round(accumulated_odometer_km, 1),
            'road_severity_multiplier': round(rough_road_severity_factor, 2),
            'effective_stress_km': round(effective_km, 1),
            'weld_crack_initiation_prob_pct': round(prob_pct, 2),
            'ndt_ultrasonic_inspection_due': is_mpi_inspection_required,
            'chassis_risk_tier': 'HIGH_CRACK_PROBABILITY' if prob_pct > 25.0 else ('MODERATE' if is_mpi_inspection_required else 'LOW_NOMINAL')
        }
