"""
CityBus Enterprise Platform - Cryptographic Hash-Chained Audit Ledger
File: backend/services/security/tamper_proof_audit_chain.py

Maintains an immutable SHA-256 cryptographic hash chain for security compliance:
- Each audit log block references the SHA-256 hash of the preceding block
- Continuous verification algorithm detects any retroactive database tampering or row deletion
- Used for financial remittances, fare modifications, and incident escalations
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class AuditBlock:
    def __init__(self, index: int, prev_hash: str, actor_id: int, action: str, details: Dict[str, Any], timestamp_iso: str = None):
        self.index = index
        self.prev_hash = prev_hash
        self.actor_id = actor_id
        self.action = action
        self.details = details
        self.timestamp = timestamp_iso or datetime.utcnow().isoformat()
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Computes SHA-256 digest of block contents."""
        block_string = json.dumps({
            'index': self.index,
            'prev_hash': self.prev_hash,
            'actor_id': self.actor_id,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()


class CryptographicAuditLedger:
    """Manages the append-only cryptographic audit chain."""

    GENESIS_HASH = "0" * 64

    def __init__(self):
        self.chain: List[AuditBlock] = []
        # Create Genesis block
        genesis = AuditBlock(index=0, prev_hash=self.GENESIS_HASH, actor_id=0, action="GENESIS_BLOCK", details={"system": "CityBus Audit Subsystem Online"})
        self.chain.append(genesis)

    def append_entry(self, actor_id: int, action: str, details: Dict[str, Any]) -> AuditBlock:
        """Appends a new verified block to the hash chain."""
        last_block = self.chain[-1]
        new_block = AuditBlock(
            index=len(self.chain),
            prev_hash=last_block.hash,
            actor_id=actor_id,
            action=action,
            details=details
        )
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self) -> Dict[str, Any]:
        """
        Verifies that no block in the audit history has been tampered with.
        """
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # 1. Check prev_hash pointer
            if curr.prev_hash != prev.hash:
                return {
                    'is_valid': False,
                    'tampered_index': i,
                    'error': f"Hash chain broken between block {i-1} and {i}."
                }

            # 2. Check block hash recomputation
            if curr.compute_hash() != curr.hash:
                return {
                    'is_valid': False,
                    'tampered_index': i,
                    'error': f"Block {i} data has been retroactively modified."
                }

        return {
            'is_valid': True,
            'total_blocks': len(self.chain),
            'latest_block_hash': self.chain[-1].hash,
            'status': 'AUDIT_INTEGRITY_VERIFIED_TAMPER_PROOF'
        }
