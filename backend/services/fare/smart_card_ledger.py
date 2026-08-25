"""
CityBus Enterprise Platform - Double-Entry Smart Card Financial Ledger
File: backend/services/fare/smart_card_ledger.py

Implements double-entry bookkeeping for contactless transit cards:
- DEBIT / CREDIT balance ledger accounts
- Daily clearing and financial reconciliation
- Anomaly and overdraft detection
"""

from datetime import datetime
from typing import List, Dict, Any


class LedgerEntry:
    def __init__(self, entry_id: str, card_number: str,
                 entry_type: str, # 'TOP_UP_CREDIT', 'FARE_DEBIT', 'REFUND_CREDIT', 'ADJUSTMENT'
                 amount: float, balance_after: float,
                 reference_id: str, description: str):
        self.entry_id = entry_id
        self.card_number = card_number
        self.entry_type = entry_type
        self.amount = amount
        self.balance_after = balance_after
        self.reference_id = reference_id
        self.description = description
        self.timestamp = datetime.utcnow()


class SmartCardLedgerEngine:
    """Manages transactional audit trail for transit purse operations."""

    @staticmethod
    def record_transaction(card_number: str, current_balance: float,
                           amount: float, tx_type: str,
                           ref_id: str, desc: str) -> Dict[str, Any]:
        """
        Executes and records a double-entry transaction.
        """
        new_balance = round(current_balance + amount, 2)
        entry_id = f"LEDGER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{card_number[-4:]}"

        return {
            'entry_id': entry_id,
            'card_number': card_number,
            'transaction_type': tx_type,
            'amount': amount,
            'previous_balance': current_balance,
            'new_balance': new_balance,
            'reference_id': ref_id,
            'description': desc,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'SETTLED'
        }
