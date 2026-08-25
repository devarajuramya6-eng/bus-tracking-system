"""
CityBus Enterprise Platform - Automated Passenger Counting (APC) Package
File: backend/services/apc/__init__.py
"""

from services.apc.infrared_door_sensor import InfraredDoorSensor
from services.apc.weight_sensor_estimator import AirSuspensionWeightEstimator
from services.apc.camera_head_detector import OverheadCameraAPC

__all__ = [
    'InfraredDoorSensor',
    'AirSuspensionWeightEstimator',
    'OverheadCameraAPC'
]
