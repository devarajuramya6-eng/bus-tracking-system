"""
CityBus Enterprise Platform - Security, RBAC & Audit Hash-Chain Tests
File: tests/test_security_audit.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.security.tamper_proof_audit_chain import CryptographicAuditLedger
from services.security.rbac_policy_enforcer import RBACPolicyEnforcer
from services.security.api_rate_limiter import APIRateLimiter


class TestSecurityAndAudit(unittest.TestCase):
    def test_cryptographic_audit_ledger_integrity(self):
        ledger = CryptographicAuditLedger()
        ledger.append_entry(actor_id=1, action="CREATE_ROUTE", details={"route": "27A"})
        ledger.append_entry(actor_id=2, action="UPDATE_FARE", details={"fare": 30.0})

        verification = ledger.verify_integrity()
        self.assertTrue(verification['is_valid'])
        self.assertEqual(verification['total_blocks'], 3)

    def test_rbac_policy_permissions(self):
        self.assertTrue(RBACPolicyEnforcer.is_authorized('super_admin', 'any:permission'))
        self.assertTrue(RBACPolicyEnforcer.is_authorized('dispatcher', 'incidents:write'))
        self.assertFalse(RBACPolicyEnforcer.is_authorized('passenger', 'buses:write'))

    def test_api_rate_limiter(self):
        limiter = APIRateLimiter(requests_per_minute=2, burst_capacity=1)
        is_limited_1, _ = limiter.is_rate_limited("client_10.0.0.1")
        is_limited_2, _ = limiter.is_rate_limited("client_10.0.0.1")
        is_limited_3, meta = limiter.is_rate_limited("client_10.0.0.1")

        self.assertFalse(is_limited_1)
        self.assertFalse(is_limited_2)
        self.assertTrue(is_limited_3)
        self.assertTrue(meta['rate_limited'])


if __name__ == '__main__':
    unittest.main()
