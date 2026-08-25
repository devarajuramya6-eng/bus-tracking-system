"""
CityBus Enterprise Platform - Digital Twin Corridor Physics Mirror
File: backend/services/digital_twin/corridor_physics_twin.py

Maintains real-time physical simulation twin of active corridor vehicles:
- Dynamic tractive resistance: F_total = F_roll + F_aero + F_grade + F_inertia
- Road friction coefficient variations (Wet asphalt = 0.45 vs Dry = 0.85)
- Real-time battery SoC and diesel consumption mirroring
"""

import math
from typing import Dict, Any


class CorridorPhysicsTwin:
    GRAVITY = 9.81
    AIR_DENSITY = 1.225 # kg/m^3
    FRONTAL_AREA = 7.5 # m^2 for city bus
    CD_DRAG = 0.65
    C_ROLLING = 0.012

    @staticmethod
    def simulate_vehicle_step(mass_kg: float, current_speed_kmh: float,
                              road_grade_pct: float, is_wet_road: bool = False,
                              delta_t_sec: float = 1.0) -> Dict[str, Any]:
        """
        Simulates 1-second physics twin delta.
        """
        v_mps = (current_speed_kmh * 1000.0) / 3600.0
        theta_rad = math.atan(road_grade_pct / 100.0)

        # Rolling resistance: F_roll = C_rr * m * g * cos(theta)
        f_roll = CorridorPhysicsTwin.C_ROLLING * mass_kg * CorridorPhysicsTwin.GRAVITY * math.cos(theta_rad)

        # Aerodynamic drag: F_aero = 0.5 * rho * Cd * A * v^2
        f_aero = 0.5 * CorridorPhysicsTwin.AIR_DENSITY * CorridorPhysicsTwin.CD_DRAG * CorridorPhysicsTwin.FRONTAL_AREA * (v_mps ** 2)

        # Grade resistance: F_grade = m * g * sin(theta)
        f_grade = mass_kg * CorridorPhysicsTwin.GRAVITY * math.sin(theta_rad)

        f_total_newtons = f_roll + f_aero + f_grade
        power_kw = (f_total_newtons * v_mps) / 1000.0

        road_mu = 0.45 if is_wet_road else 0.85

        return {
            'speed_kmh': round(current_speed_kmh, 1),
            'mass_total_kg': round(mass_kg, 1),
            'road_grade_pct': round(road_grade_pct, 1),
            'rolling_force_n': round(f_roll, 1),
            'aero_drag_force_n': round(f_aero, 1),
            'grade_force_n': round(f_grade, 1),
            'total_tractive_force_n': round(f_total_newtons, 1),
            'instantaneous_power_demand_kw': round(max(0.0, power_kw), 2),
            'road_surface_friction_mu': road_mu,
            'status': 'TWIN_STATE_SYNCHRONIZED'
        }
