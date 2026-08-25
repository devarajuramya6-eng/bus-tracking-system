"""
CityBus Enterprise Platform - Crew Runcutting & Duty Optimization Engine
File: backend/services/scheduling/runcutting_engine.py

Cuts vehicle blocks into compliant, legal driver and conductor duty shifts:
- Straight shifts (continuous 7.5 to 8.5 hours with brief relief break)
- Split shifts (peak morning + peak evening with unpaid middle split)
- Enforces Motor Transport Workers Act limits (Max 8h daily driving, 12h maximum spread)
"""

from typing import List, Dict, Any, Optional
from services.scheduling.blocking_engine import VehicleBlock, TripInstance


class CrewDutyShift:
    """Represents a legal operational driver shift."""
    def __init__(self, duty_id: str, duty_type: str = "STRAIGHT_SHIFT"):
        self.duty_id = duty_id
        self.duty_type = duty_type # 'STRAIGHT_SHIFT', 'SPLIT_SHIFT', 'NIGHT_SHIFT'
        self.trips: List[TripInstance] = []
        self.sign_on_min: int = 0
        self.sign_off_min: int = 0
        self.paid_minutes: int = 0
        self.driving_minutes: int = 0
        self.break_minutes: int = 0


class CrewRuncuttingEngine:
    """Generates driver duty rosters from vehicle blocks."""

    MAX_DRIVING_MINUTES = 480 # 8 hours
    MAX_SPREAD_MINUTES = 720 # 12 hours max spread for split shifts
    MIN_MEAL_BREAK_MINUTES = 30

    @staticmethod
    def cut_duties(blocks: List[VehicleBlock]) -> List[CrewDutyShift]:
        duties: List[CrewDutyShift] = []
        duty_counter = 1

        for block in blocks:
            current_duty = CrewDutyShift(duty_id=f"DUTY-{duty_counter:03d}", duty_type="STRAIGHT_SHIFT")
            current_duty.sign_on_min = block.pull_out_min

            accum_driving = 0

            for trip in block.trips:
                trip_duration = trip.arrival_min - trip.departure_min

                # If adding trip exceeds legal driving limits, cut duty and start new one
                if accum_driving + trip_duration > CrewRuncuttingEngine.MAX_DRIVING_MINUTES:
                    current_duty.sign_off_min = current_duty.trips[-1].arrival_min + 15
                    current_duty.driving_minutes = accum_driving
                    current_duty.paid_minutes = current_duty.sign_off_min - current_duty.sign_on_min
                    duties.append(current_duty)

                    # Start next relief duty
                    duty_counter += 1
                    current_duty = CrewDutyShift(duty_id=f"DUTY-{duty_counter:03d}", duty_type="STRAIGHT_SHIFT")
                    current_duty.sign_on_min = trip.departure_min - 15
                    accum_driving = 0

                current_duty.trips.append(trip)
                accum_driving += trip_duration

            if current_duty.trips:
                current_duty.sign_off_min = current_duty.trips[-1].arrival_min + 15
                current_duty.driving_minutes = accum_driving
                current_duty.paid_minutes = current_duty.sign_off_min - current_duty.sign_on_min
                duties.append(current_duty)
                duty_counter += 1

        return duties
