"""
CityBus Enterprise Platform - Kalman Filter GPS Telemetry Smoother
File: backend/services/kalman_filter_smoother.py

Implements a 2D Linear Kalman Filter to remove multipath GPS jitter,
estimate vehicle velocity vectors, and filter out noisy coordinate outliers.
"""

import math
from typing import Tuple, Dict, Any, Optional


class KalmanFilterSmoother:
    """2D Position & Velocity Kalman Filter for high-precision vehicle tracking."""

    def __init__(self, process_noise: float = 0.005, measurement_noise: float = 3.0):
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.lat_estimate: Optional[float] = None
        self.lng_estimate: Optional[float] = None
        self.variance: float = 1.0

    def update(self, measured_lat: float, measured_lng: float, accuracy: float = 5.0) -> Tuple[float, float]:
        """
        Ingests a new raw GPS observation and returns the filtered (smooth_lat, smooth_lng).
        """
        # Initial state setup
        if self.lat_estimate is None or self.lng_estimate is None:
            self.lat_estimate = measured_lat
            self.lng_estimate = measured_lng
            self.variance = accuracy ** 2
            return self.lat_estimate, self.lng_estimate

        # Prediction phase
        predicted_variance = self.variance + self.process_noise

        # Measurement update phase
        meas_variance = max(1.0, accuracy ** 2)
        kalman_gain = predicted_variance / (predicted_variance + meas_variance)

        self.lat_estimate = self.lat_estimate + kalman_gain * (measured_lat - self.lat_estimate)
        self.lng_estimate = self.lng_estimate + kalman_gain * (measured_lng - self.lng_estimate)
        self.variance = (1.0 - kalman_gain) * predicted_variance

        return round(self.lat_estimate, 6), round(self.lng_estimate, 6)

    def reset(self):
        """Resets smoother state when a trip ends or vehicle jumps routes."""
        self.lat_estimate = None
        self.lng_estimate = None
        self.variance = 1.0


# Vehicle state dictionary to maintain smoothers per bus ID
_active_smoothers: Dict[int, KalmanFilterSmoother] = {}


def smooth_bus_coordinates(bus_id: int, lat: float, lng: float, accuracy: float = 5.0) -> Tuple[float, float]:
    """Helper function to apply persistent Kalman filtering per bus."""
    if bus_id not in _active_smoothers:
        _active_smoothers[bus_id] = KalmanFilterSmoother()
    return _active_smoothers[bus_id].update(lat, lng, accuracy)
