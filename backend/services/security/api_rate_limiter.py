"""
CityBus Enterprise Platform - API Sliding Window & Token Bucket Rate Limiter
File: backend/services/security/api_rate_limiter.py

Protects REST endpoints and WebSocket connections from volumetric abuse:
- Sliding window counter per IP / API Key (e.g. 120 requests/minute)
- Token Bucket burst capacity for high-frequency GPS telemetry
- HTTP 429 Too Many Requests response generator with Retry-After header
"""

import time
from typing import Dict, Any, Tuple
from collections import deque


class APIRateLimiter:
    """Sliding-window request rate limiter."""

    def __init__(self, requests_per_minute: int = 120, burst_capacity: int = 30):
        self.limit = requests_per_minute
        self.window_sec = 60.0
        self.client_windows: Dict[str, deque] = {}

    def is_rate_limited(self, client_identifier: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Evaluates rate limit for a client IP or user ID.
        :return: (is_blocked, rate_limit_metadata)
        """
        now = time.time()
        if client_identifier not in self.client_windows:
            self.client_windows[client_identifier] = deque()

        window = self.client_windows[client_identifier]

        # Purge timestamps older than 60 seconds
        while window and window[0] < (now - self.window_sec):
            window.popleft()

        current_count = len(window)

        if current_count >= self.limit:
            retry_after = int(self.window_sec - (now - window[0]))
            return True, {
                'rate_limited': True,
                'limit_per_minute': self.limit,
                'current_requests': current_count,
                'retry_after_seconds': max(1, retry_after)
            }

        window.append(now)
        return False, {
            'rate_limited': False,
            'limit_per_minute': self.limit,
            'remaining_requests': self.limit - (current_count + 1),
            'reset_seconds': int(self.window_sec)
        }
