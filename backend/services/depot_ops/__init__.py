"""
CityBus Enterprise Platform - Depot Operations & Fleet Logistics Package
File: backend/services/depot_ops/__init__.py
"""

from services.depot_ops.bay_parking_optimizer import DepotParkingOptimizer
from services.depot_ops.daily_dispatch_roster import DailyDispatchRosterManager
from services.depot_ops.fuel_bowser_automation import FuelBowserAutomationEngine

__all__ = [
    'DepotParkingOptimizer',
    'DailyDispatchRosterManager',
    'FuelBowserAutomationEngine'
]
