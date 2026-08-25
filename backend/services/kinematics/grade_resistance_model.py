"""
CityBus Enterprise Platform - Heavy Vehicle Dynamics & Tractive Effort Physics
File: backend/services/kinematics/grade_resistance_model.py

Models physical forces acting on commercial transit buses:
- Aerodynamic Drag Force (N)
- Rolling Resistance Force (N)
- Road Gradient Climbing / Decent Force (N)
- Inertial Acceleration Force (N)
- Instantaneous Engine / Motor Mechanical Power (kW) and Torque (Nm)
"""

import math
from typing import Dict, Any


class VehiclePhysicsModel:
    """Calculates instantaneous road-load tractive forces."""

    AIR_DENSITY_KG_M3 = 1.205 # At sea level 20°C
    GRAVITY_M_S2 = 9.80665

    # Heavy Transit Bus Parameters (12-meter Low Floor Bus)
    BUS_FRONTAL_AREA_M2 = 7.5
    DRAG_COEFFICIENT_CD = 0.65
    ROLLING_RESISTANCE_CRR = 0.009
    CURB_WEIGHT_KG = 12000.0
    PASSENGER_AVG_WEIGHT_KG = 68.0

    @staticmethod
    def calculate_tractive_effort(speed_kmh: float,
                                  accel_mps2: float,
                                  passenger_count: int,
                                  road_grade_pct: float = 0.0) -> Dict[str, Any]:
        """
        Computes total tractive force and power requirement.
        :param speed_kmh: Vehicle speed in km/h
        :param accel_mps2: Forward acceleration in m/s^2
        :param passenger_count: Current passenger count
        :param road_grade_pct: Road slope percentage (e.g. 3.0 for 3% uphill incline)
        """
        v_mps = max(0.0, speed_kmh / 3.6)
        total_mass_kg = VehiclePhysicsModel.CURB_WEIGHT_KG + (passenger_count * VehiclePhysicsModel.PASSENGER_AVG_WEIGHT_KG)

        # 1. Aerodynamic Drag: F_aero = 0.5 * rho * Cd * A * v^2
        f_aero = 0.5 * VehiclePhysicsModel.AIR_DENSITY_KG_M3 * VehiclePhysicsModel.DRAG_COEFFICIENT_CD * VehiclePhysicsModel.BUS_FRONTAL_AREA_M2 * (v_mps ** 2)

        # Road slope angle theta = atan(grade / 100)
        theta_rad = math.atan(road_grade_pct / 100.0)

        # 2. Rolling Resistance: F_roll = Crr * m * g * cos(theta)
        f_roll = VehiclePhysicsModel.ROLLING_RESISTANCE_CRR * total_mass_kg * VehiclePhysicsModel.GRAVITY_M_S2 * math.cos(theta_rad)

        # 3. Grade Force: F_grade = m * g * sin(theta)
        f_grade = total_mass_kg * VehiclePhysicsModel.GRAVITY_M_S2 * math.sin(theta_rad)

        # 4. Acceleration Force: F_accel = m * a * (1 + rotational_inertia_factor 0.10)
        f_accel = total_mass_kg * accel_mps2 * 1.10

        total_tractive_force_n = f_aero + f_roll + f_grade + f_accel
        # Instantaneous Power = Force * Velocity (Watts -> kW)
        power_kw = (total_tractive_force_n * v_mps) / 1000.0 if total_tractive_force_n > 0 else 0.0

        return {
            'total_mass_kg': round(total_mass_kg, 1),
            'speed_kmh': round(speed_kmh, 1),
            'road_grade_pct': road_grade_pct,
            'f_aero_newtons': round(f_aero, 1),
            'f_roll_newtons': round(f_roll, 1),
            'f_grade_newtons': round(f_grade, 1),
            'f_accel_newtons': round(f_accel, 1),
            'total_tractive_force_n': round(total_tractive_force_n, 1),
            'required_power_kw': round(power_kw, 2)
        }
