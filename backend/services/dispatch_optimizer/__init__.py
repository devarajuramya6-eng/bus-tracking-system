"""
CityBus Enterprise Platform - Multi-Depot Dispatch & Deadhead Optimization Package
File: backend/services/dispatch_optimizer/__init__.py
"""

from services.dispatch_optimizer.hungarian_depot_assignment import HungarianDepotAssigner
from services.dispatch_optimizer.driver_shift_relief_station_sync import DriverReliefSyncEngine
from services.dispatch_optimizer.emergency_spare_bus_insertion import StandbySpareBusManager

__all__ = [
    'HungarianDepotAssigner',
    'DriverReliefSyncEngine',
    'StandbySpareBusManager'
]
