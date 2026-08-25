"""
CityBus Enterprise Platform - Preventive Major Overhaul Milestone Tracker
File: backend/services/asset_lifecycle/major_overhaul_milestone_tracker.py

Tracks major mechanical overhauls based on cumulative vehicle mileage:
- Schedule 1 (100,000 km): Fuel injector overhaul & alternator rebuild
- Schedule 2 (250,000 km): Transmission differential rebuild & leaf spring recambering
- Schedule 3 (500,000 km): Complete engine block cylinder boring & crankshaft grinding
"""

from typing import Dict, Any, List


class OverhaulMilestoneTracker:
    OVERHAUL_MILESTONES = [
        {'milestone_km': 100000, 'name': 'Mid-Life Injection & Alternator Service', 'downtime_days': 2},
        {'milestone_km': 250000, 'name': 'Transmission & Differential Major Overhaul', 'downtime_days': 4},
        {'milestone_km': 500000, 'name': 'Complete Engine Block Rebuild (MOH-1)', 'downtime_days': 7}
    ]

    @staticmethod
    def evaluate_bus_mileage(bus_number: str, odometer_km: float) -> Dict[str, Any]:
        """
        Identifies next pending major overhaul milestone.
        """
        for m in OverhaulMilestoneTracker.OVERHAUL_MILESTONES:
            diff_km = m['milestone_km'] - odometer_km
            if -5000 <= diff_km <= 5000: # Within 5,000 km window
                return {
                    'bus_number': bus_number,
                    'odometer_km': round(odometer_km, 1),
                    'milestone_due': m['name'],
                    'milestone_target_km': m['milestone_km'],
                    'km_difference': round(diff_km, 1),
                    'est_workshop_downtime_days': m['downtime_days'],
                    'status': 'OVERHAUL_WORK_ORDER_TRIGGERED'
                }

        return {
            'bus_number': bus_number,
            'odometer_km': round(odometer_km, 1),
            'milestone_due': 'None in current window',
            'status': 'STANDARD_PERIODIC_MAINTENANCE'
        }
