"""
CityBus Enterprise Platform - Automated Fare Collection (AFC) & Smart Card Service
File: backend/services/smart_card_afc_service.py

Implements National Common Mobility Card (NCMC) / Mifare DESFire standards:
- Contactless smart card balance inquiry and top-up
- Cryptographic SAM (Secure Access Module) token authentication
- Tap-in / Tap-out distance-based fare deduction with anti-passback guards
- Offline card validation transaction logging
"""

import hmac
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from models import User, Ticket, db
from repositories.audit_repository import AuditRepository


class SmartCardRecord:
    def __init__(self, card_uid: str, user_id: int, balance: float = 200.0, card_type: str = "NCMC"):
        self.card_uid = card_uid
        self.user_id = user_id
        self.balance = balance
        self.card_type = card_type  # NCMC, STUDENT_PASS, SENIOR_CITIZEN
        self.status = "ACTIVE"
        self.last_tap_time: Optional[datetime] = None
        self.current_trip_origin_stop: Optional[str] = None
        self.current_trip_bus_id: Optional[int] = None


class SmartCardAFCService:
    """Manages contactless NCMC transit cards and terminal transaction validation."""

    HMAC_SECRET = b"citybus_sam_hsm_diversified_key_2026"
    _card_registry: Dict[str, SmartCardRecord] = {}

    @classmethod
    def get_or_register_card(cls, card_uid: str, user_id: int, initial_balance: float = 250.0, card_type: str = "NCMC") -> SmartCardRecord:
        """Registers a new smart card or fetches existing card record."""
        clean_uid = card_uid.strip().upper()
        if clean_uid not in cls._card_registry:
            cls._card_registry[clean_uid] = SmartCardRecord(clean_uid, user_id, initial_balance, card_type)
            AuditRepository.log_event("SMART_CARD_REGISTERED", "SmartCard", clean_uid, user_id, None, f"Type: {card_type}")
        return cls._card_registry[clean_uid]

    @classmethod
    def process_tap_in(cls, card_uid: str, bus_id: int, stop_name: str) -> Dict[str, Any]:
        """
        Handles boarding tap-in: verifies minimum balance, sets active journey start node.
        """
        clean_uid = card_uid.strip().upper()
        card = cls._card_registry.get(clean_uid)
        if not card:
            return {"success": False, "code": "CARD_NOT_FOUND", "message": "Unregistered transit card"}

        if card.status != "ACTIVE":
            return {"success": False, "code": "CARD_BLOCKED", "message": "Card is suspended or blocked"}

        # Anti-passback check (minimum 60s between duplicate taps)
        if card.last_tap_time and (datetime.utcnow() - card.last_tap_time).total_seconds() < 60:
            return {"success": False, "code": "PASSBACK_VIOLATION", "message": "Card tapped too recently"}

        if card.balance < 15.0:
            return {"success": False, "code": "INSUFFICIENT_BALANCE", "message": "Minimum ₹15.00 balance required"}

        card.last_tap_time = datetime.utcnow()
        card.current_trip_origin_stop = stop_name
        card.current_trip_bus_id = bus_id

        # Generate SAM HMAC Authorization Signature
        auth_sig = cls._generate_sam_mac(clean_uid, bus_id, card.balance)

        AuditRepository.log_event("AFC_TAP_IN", "SmartCard", clean_uid, card.user_id, None, f"Bus: {bus_id}, Stop: {stop_name}")

        return {
            "success": True,
            "card_uid": clean_uid,
            "action": "TAP_IN",
            "origin_stop": stop_name,
            "remaining_balance": card.balance,
            "auth_signature": auth_sig
        }

    @classmethod
    def process_tap_out(cls, card_uid: str, bus_id: int, stop_name: str, distance_km: float = 8.0) -> Dict[str, Any]:
        """
        Handles alighting tap-out: calculates fare, deducts balance, and generates digital receipt.
        """
        clean_uid = card_uid.strip().upper()
        card = cls._card_registry.get(clean_uid)
        if not card:
            return {"success": False, "code": "CARD_NOT_FOUND", "message": "Card not found"}

        origin_stop = card.current_trip_origin_stop or "Central Terminal"
        fare_inr = round(max(10.0, 10.0 + (distance_km * 1.5)), 2)

        # Apply concession
        if card.card_type == "STUDENT_PASS":
            fare_inr = round(fare_inr * 0.5, 2)
        elif card.card_type == "SENIOR_CITIZEN":
            fare_inr = round(fare_inr * 0.7, 2)

        card.balance = round(card.balance - fare_inr, 2)
        card.current_trip_origin_stop = None
        card.current_trip_bus_id = None
        card.last_tap_time = datetime.utcnow()

        AuditRepository.log_event("AFC_TAP_OUT", "SmartCard", clean_uid, card.user_id, None, f"Fare: ₹{fare_inr}")

        return {
            "success": True,
            "card_uid": clean_uid,
            "action": "TAP_OUT",
            "origin_stop": origin_stop,
            "destination_stop": stop_name,
            "fare_deducted": fare_inr,
            "remaining_balance": card.balance
        }

    @classmethod
    def top_up_balance(cls, card_uid: str, amount_inr: float, payment_ref: str) -> Dict[str, Any]:
        """Adds funds to the card's stored-value purse."""
        clean_uid = card_uid.strip().upper()
        card = cls._card_registry.get(clean_uid)
        if not card:
            return {"success": False, "message": "Card not found"}

        card.balance = round(card.balance + amount_inr, 2)
        AuditRepository.log_event("AFC_TOP_UP", "SmartCard", clean_uid, card.user_id, None, f"Amount: ₹{amount_inr}, Ref: {payment_ref}")

        return {
            "success": True,
            "card_uid": clean_uid,
            "top_up_amount": amount_inr,
            "new_balance": card.balance,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def _generate_sam_mac(cls, card_uid: str, bus_id: int, balance: float) -> str:
        """Computes HMAC-SHA256 authorization token."""
        msg = f"{card_uid}|{bus_id}|{balance}|{int(time.time())}".encode('utf-8')
        return hmac.new(cls.HMAC_SECRET, msg, hashlib.sha256).hexdigest()[:16]
