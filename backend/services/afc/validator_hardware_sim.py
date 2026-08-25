"""
CityBus Enterprise Platform - Contactless NCMC & EMV Validator Hardware Simulator
File: backend/services/afc/validator_hardware_sim.py

Emulates ISO/IEC 14443 Type A/B contactless smart card transaction cycles:
- APDU Command/Response exchange (SELECT PPSE, READ BALANCE, DEBIT PURSE)
- Sub-300ms transaction cycle verification
- Onboard validator audio-visual feedback signals (Green LED/Single Beep, Red LED/Double Beep)
"""

import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime


class ContactlessValidatorSimulator:
    """Simulates physical onboard bus electronic ticket validator (ETV)."""

    def __init__(self, device_id: str = "ETV-VJA-8042", bus_id: int = 1):
        self.device_id = device_id
        self.bus_id = bus_id
        self.is_online = True
        self.offline_transaction_buffer = []

    def process_tap(self, card_uid: str, card_type: str, current_balance: float,
                    fare_amount: float, stop_name: str, route_number: str) -> Dict[str, Any]:
        """
        Executes a complete contactless card tap cycle.
        """
        start_time = time.time()
        tx_id = f"TX-NCMC-{uuid.uuid4().hex[:10].upper()}"

        # ISO 7816-4 APDU Response Code Simulation: 0x9000 (Success), 0x6A82 (Not Found), 0x6985 (Conditions not satisfied)
        if current_balance < fare_amount:
            elapsed_ms = int((time.time() - start_time) * 1000) + 120
            return {
                'status': 'DECLINED',
                'reason': 'INSUFFICIENT_BALANCE',
                'apdu_sw': '0x6985',
                'audio_signal': 'DOUBLE_HIGH_BEEP_ERROR',
                'led_color': 'RED',
                'card_uid': card_uid,
                'fare_deducted': 0.0,
                'remaining_balance': current_balance,
                'latency_ms': elapsed_ms,
                'message': 'Insufficient Balance. Please top up your transit card.'
            }

        new_balance = round(current_balance - fare_amount, 2)
        elapsed_ms = int((time.time() - start_time) * 1000) + 185 # Realistic ~185ms tap-in latency

        receipt = {
            'status': 'APPROVED',
            'transaction_id': tx_id,
            'apdu_sw': '0x9000',
            'audio_signal': 'SINGLE_BEEP_SUCCESS',
            'led_color': 'GREEN',
            'device_id': self.device_id,
            'bus_id': self.bus_id,
            'route_number': route_number,
            'boarding_stop': stop_name,
            'card_uid': card_uid,
            'card_type': card_type,
            'fare_deducted': fare_amount,
            'remaining_balance': new_balance,
            'timestamp': datetime.utcnow().isoformat(),
            'latency_ms': elapsed_ms,
            'message': f"Boarded at {stop_name}. Deducted ₹{fare_amount:.2f}. Balance: ₹{new_balance:.2f}"
        }

        self.offline_transaction_buffer.append(receipt)
        return receipt
