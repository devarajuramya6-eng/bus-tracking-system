"""
CityBus Enterprise Platform - Smart Card Cashback & Loyalty Reward Engine
File: backend/services/smart_card_cashback_reward_service.py

Calculates monthly milestone cashbacks (₹50 cashback after 30 bus rides),
converts green commute loyalty points to stored-value purse credits, and manages merchant partner perks.
"""

from typing import Dict, List, Any, Optional
from repositories.audit_repository import AuditRepository


class SmartCardCashbackRewardService:
    """Manages commuter rewards and wallet cashback incentives."""

    @staticmethod
    def evaluate_monthly_cashback(card_uid: str, monthly_tap_count: int, total_spend_inr: float) -> Dict[str, Any]:
        """Calculates earned wallet cashback credits."""
        cashback_inr = 0.0
        tier = "BRONZE"

        if monthly_tap_count >= 50:
            cashback_inr = round(total_spend_inr * 0.10, 2) # 10% Gold cashback
            tier = "GOLD"
        elif monthly_tap_count >= 30:
            cashback_inr = round(total_spend_inr * 0.05, 2) # 5% Silver cashback
            tier = "SILVER"

        AuditRepository.log_event("CASHBACK_AWARDED", "SmartCardReward", card_uid, None, None, f"Amount: ₹{cashback_inr}, Tier: {tier}")

        return {
            "card_uid": card_uid,
            "monthly_taps": monthly_tap_count,
            "total_transit_spend_inr": total_spend_inr,
            "commuter_tier": tier,
            "cashback_earned_inr": cashback_inr,
            "auto_credited_to_purse": True
        }
