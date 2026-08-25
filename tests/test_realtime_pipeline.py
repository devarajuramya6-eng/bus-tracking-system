"""
CityBus Enterprise Platform - Realtime Pipeline & Redis Event Bus Tests
File: tests/test_realtime_pipeline.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from realtime.redis_event_bus import RedisEventBus
from realtime.telemetry_pipeline import TelemetryIngestionPipeline


class TestRealtimeEventStreaming(unittest.TestCase):
    def test_redis_event_bus_pub_sub(self):
        bus = RedisEventBus()
        received_messages = []

        def on_location_ping(data):
            received_messages.append(data)

        bus.subscribe('bus:location', on_location_ping)
        bus.publish('bus:location', {'bus_id': 1, 'speed': 42.0})

        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0]['bus_id'], 1)

    def test_telemetry_ingestion_pipeline_valid_and_anomalies(self):
        pipeline = TelemetryIngestionPipeline(buffer_capacity=100, batch_size=10)

        # Valid ping in Andhra Pradesh
        valid = pipeline.ingest_ping(bus_id=1, lat=16.5062, lng=80.6480, speed=35.0, heading=90.0)
        self.assertTrue(valid)

        # Invalid ping (Out of bounds coordinates)
        invalid = pipeline.ingest_ping(bus_id=1, lat=88.5062, lng=150.6480, speed=35.0, heading=90.0)
        self.assertFalse(invalid)
        self.assertEqual(pipeline.dropped_anomalies, 1)

        batch = pipeline.flush_batch()
        self.assertEqual(len(batch), 1)
        self.assertEqual(batch[0]['bus_id'], 1)


if __name__ == '__main__':
    unittest.main()
