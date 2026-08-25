"""
CityBus Enterprise Platform - Friction & Regenerative Brake Torque Blending Engine
File: backend/services/regenerative_braking/regen_torque_blending.py

Blends electronic motor regenerative braking with pneumatic friction disc brakes:
- Low-to-Medium Braking (0-40% Pedal): 100% Electric motor regeneration (Zero brake pad wear)
- Heavy Deceleration (> 40% Pedal): Blends friction pneumatic discs for maximum stopping power
- High Battery SoC Derating: Tapers regenerative torque above 92% SoC to prevent battery overvoltage
"""

from typing import Dict, Any


class RegenTorqueBlendingEngine:
    MAX_ELECTRIC_MOTOR_TORQUE_NM = 2800.0 # Heavy e-bus traction motor peak regen

    @staticmethod
    def blend_brake_torque(pedal_displacement_pct: float,
                           vehicle_speed_kmh: float,
                           battery_soc_pct: float) -> Dict[str, Any]:
        """
        Calculates regenerative vs friction braking split.
        """
        clamped_pedal = max(0.0, min(100.0, pedal_displacement_pct))
        total_demanded_torque_nm = (clamped_pedal / 100.0) * 6000.0 # Max 6,000 Nm total brake torque

        # SoC regen derating factor (1.0 below 90%, scales to 0.0 at 98%)
        if battery_soc_pct >= 98.0:
            soc_factor = 0.0
        elif battery_soc_pct > 90.0:
            soc_factor = (98.0 - battery_soc_pct) / 8.0
        else:
            soc_factor = 1.0

        # Speed cutoff: Regen ineffective below 5 km/h
        speed_factor = 1.0 if vehicle_speed_kmh >= 10.0 else max(0.0, (vehicle_speed_kmh - 5.0) / 5.0)

        max_avail_regen = RegenTorqueBlendingEngine.MAX_ELECTRIC_MOTOR_TORQUE_NM * soc_factor * speed_factor
        regen_torque_nm = min(total_demanded_torque_nm, max_avail_regen)
        friction_torque_nm = max(0.0, total_demanded_torque_nm - regen_torque_nm)

        regen_share_pct = (regen_torque_nm / max(1.0, total_demanded_torque_nm)) * 100.0

        return {
            'pedal_displacement_pct': round(clamped_pedal, 1),
            'total_brake_torque_nm': round(total_demanded_torque_nm, 1),
            'regenerative_torque_nm': round(regen_torque_nm, 1),
            'friction_pneumatic_torque_nm': round(friction_torque_nm, 1),
            'regenerative_share_pct': round(regen_share_pct, 1),
            'battery_soc_pct': round(battery_soc_pct, 1),
            'is_brake_pad_wear_prevented': friction_torque_nm == 0.0 and clamped_pedal > 0
        }
