"""
CityBus Enterprise Platform - Transit Notifications & Alert Tests
File: tests/test_transit_notifications.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.transit_notifications.web_push_vapid_broadcaster import WebPushVAPIDBroadcaster
from services.transit_notifications.telegram_whatsapp_bot_dispatch import CommuterBotDispatcher
from services.transit_notifications.sms_cell_broadcast_emergency import EmergencyCellBroadcastSender


class TestTransitNotifications(unittest.TestCase):
    def test_web_push_vapid_formatting(self):
        push = WebPushVAPIDBroadcaster.build_push_payload(
            title="Bus 27A Arriving",
            body="Your bus will arrive at Benz Circle in 3 minutes.",
            action_url="/tracker?bus=AP16-001",
            topic_category="STOP_ARRIVAL_ALERT"
        )
        self.assertEqual(push['notification']['title'], "Bus 27A Arriving")
        self.assertEqual(push['vapid_headers']['Urgency'], 'high')

    def test_commuter_bot_dispatcher_tracking_intent(self):
        reply = CommuterBotDispatcher.process_incoming_query(
            channel="WHATSAPP",
            sender_phone_or_id="+919876543210",
            message_text="where is 27A?"
        )
        self.assertEqual(reply['detected_intent'], 'BUS_LIVE_TRACKING')
        self.assertTrue(reply['is_auto_replied'])
        self.assertIn('27A', reply['response_english'])

    def test_emergency_cell_broadcast_packet(self):
        cbs = EmergencyCellBroadcastSender.build_cell_broadcast_packet(
            alert_type="CYCLONE_ALERT",
            geo_cell_ids=["CELL_VJA_01", "CELL_VJA_02"],
            alert_message_en="Emergency Warning: Severe cyclone approaching. Free transit evacuations active.",
            alert_message_te="తీవ్ర తుఫాను హెచ్చరిక. ఉచిత రవాణా అందుబాటులో ఉంది."
        )
        self.assertEqual(cbs['cbs_message_id'], 4370)
        self.assertEqual(cbs['target_cell_towers_count'], 2)
        self.assertTrue(cbs['is_high_priority_presidential_alert'])


if __name__ == '__main__':
    unittest.main()
