from typing import Dict, List, Any
from models import Bus, db

class DepotOilSamplingLaboratoryService:
    """Processes spectrographic oil analysis to detect engine wear metals (Iron, Copper, Lead)."""

    @staticmethod
    def analyze_oil_sample(bus_id: int, iron_ppm: float = 24.0, copper_ppm: float = 8.5, soot_pct: float = 1.2) -> Dict[str, Any]:
        bus = Bus.query.get(bus_id)
        bus_num = bus.bus_number if bus else f"Bus #{bus_id}"

        viscosity_cst = 14.2 # 15W-40 nominal at 100°C
        status = "NORMAL"

        if iron_ppm > 50.0 or soot_pct > 3.0:
            status = "ACTION_REQUIRED_EARLY_OIL_CHANGE"
        elif iron_ppm > 80.0:
            status = "CRITICAL_BEARING_WEAR_WARNING"

        return {
            "bus_id": bus_id,
            "bus_number": bus_num,
            "kinematic_viscosity_cst": viscosity_cst,
            "iron_wear_ppm": iron_ppm,
            "copper_wear_ppm": copper_ppm,
            "soot_percentage": soot_pct,
            "fluid_health_status": status,
            "next_sampling_odometer_km": (bus.odometer_km or 0) + 15000
        }
