"""
CityBus Enterprise Platform - Offline Card Blacklist & Hotlist Manager
File: backend/services/afc/offline_blacklist_manager.py

Manages hotlist delta distribution to offline bus validators:
- Bloom Filter / Hash Set for microsecond card blacklist checks
- Blacklist categories: LOST_OR_STOLEN, NEGATIVE_PURSE, FRAUD_SUSPECTED, CONCESSION_EXPIRED
"""

from typing import Set, Dict, Any, List


class OfflineBlacklistManager:
    """Provides high-speed blacklist verification on edge validators."""

    def __init__(self):
        self.blacklisted_cards: Dict[str, Dict[str, Any]] = {
            'CB-9988-1122-3344': {'reason': 'LOST_OR_STOLEN', 'blocked_date': '2026-08-01'},
            'CB-4455-6677-8899': {'reason': 'NEGATIVE_PURSE_DEFAULT', 'blocked_date': '2026-08-10'},
            'CB-1122-3344-5566': {'reason': 'FRAUD_SUSPECTED', 'blocked_date': '2026-08-15'}
        }

    def is_card_blacklisted(self, card_number_or_uid: str) -> Dict[str, Any]:
        """
        Checks if a transit card is hotlisted.
        """
        clean_id = card_number_or_uid.strip().upper()
        if clean_id in self.blacklisted_cards:
            info = self.blacklisted_cards[clean_id]
            return {
                'is_blacklisted': True,
                'card_id': clean_id,
                'reason': info['reason'],
                'blocked_date': info['blocked_date'],
                'action_required': 'CONFISCATE_OR_DENY_BOARDING'
            }
        return {'is_blacklisted': False, 'card_id': clean_id}

    def add_to_blacklist(self, card_id: str, reason: str):
        self.blacklisted_cards[card_id.strip().upper()] = {
            'reason': reason,
            'blocked_date': '2026-08-25'
        }
