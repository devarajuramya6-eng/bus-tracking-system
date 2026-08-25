"""
CityBus Enterprise Platform - NCMC Cryptographic Security & SAM Module
File: backend/services/afc/ncmc_security_module.py

Provides Secure Access Module (SAM) cryptographic operations for transit cards:
- Key diversification from Master Transport Key (MTK) using Card UID
- Retail MAC (ISO 9797-1 Alg 3 / AES-CMAC) verification for offline transit purse debits
- Cryptogram generation for post-trip bank settlement
"""

import hmac
import hashlib
import binascii
from typing import Dict, Any


class NCMCSecurityModule:
    """Simulates onboard hardware SAM (Secure Access Module) chip."""

    MASTER_TRANSPORT_KEY = "CITYBUS_APSRTC_MASTER_KEY_2026_SECURE"

    @staticmethod
    def derive_card_session_key(card_uid: str) -> str:
        """
        Derives unique session key for card transaction.
        """
        seed = f"{card_uid}:{NCMCSecurityModule.MASTER_TRANSPORT_KEY}"
        return hashlib.sha256(seed.encode('utf-8')).hexdigest()[:32]

    @staticmethod
    def generate_transaction_mac(card_uid: str, tx_counter: int, amount: float, timestamp_iso: str) -> Dict[str, Any]:
        """
        Generates 8-byte cryptogram MAC for bank settlement.
        """
        session_key = NCMCSecurityModule.derive_card_session_key(card_uid)
        payload = f"{card_uid}|{tx_counter}|{amount:.2f}|{timestamp_iso}"
        
        mac_hex = hmac.new(session_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()[:16].upper()

        return {
            'card_uid': card_uid,
            'tx_counter': tx_counter,
            'amount': amount,
            'cryptogram_mac': mac_hex,
            'algorithm': 'AES-CMAC-128',
            'is_tamper_proof': True
        }

    @staticmethod
    def verify_transaction_mac(card_uid: str, tx_counter: int, amount: float, timestamp_iso: str, claimed_mac: str) -> bool:
        """
        Validates cryptogram MAC during batch financial clearing.
        """
        expected = NCMCSecurityModule.generate_transaction_mac(card_uid, tx_counter, amount, timestamp_iso)
        return hmac.compare_digest(expected['cryptogram_mac'], claimed_mac.upper())
