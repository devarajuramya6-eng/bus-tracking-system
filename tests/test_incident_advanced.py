"""
CityBus Enterprise Platform - Advanced Incident Triage & Forensic Blackbox Tests
File: tests/test_incident_advanced.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.incidents_adv.incident_triage_engine import IncidentTriageEngine
from services.incidents_adv.accident_reconstruction import BlackboxTelemetryReconstructor
from services.incidents_adv.insurance_claim_packager import InsuranceClaimsPackager


class TestAdvancedIncidents(unittest.TestCase):
    def test_incident_triage_critical(self):
        triage = IncidentTriageEngine.triage_incident(
            incident_category="FIRE_IN_ENGINE_BAY",
            description="Driver noticed smoke at rear",
            passengers_affected=30
        )
        self.assertEqual(triage['severity_level'], 4)
        self.assertEqual(triage['severity_name'], 'CRITICAL')
        self.assertTrue(triage['requires_executive_escalation'])

    def test_blackbox_crash_reconstruction(self):
        stream = [
            {'timestamp': '10:00:01', 'speed': 42.0, 'ax_g': 0.1, 'brake_active': False},
            {'timestamp': '10:00:02', 'speed': 41.0, 'ax_g': -0.2, 'brake_active': True},
            {'timestamp': '10:00:03', 'speed': 15.0, 'ax_g': -0.85, 'brake_active': True},
            {'timestamp': '10:00:04', 'speed': 0.0, 'ax_g': -1.2, 'brake_active': True}
        ]
        recon = BlackboxTelemetryReconstructor.reconstruct_event(stream, crash_event_index=3)
        self.assertEqual(recon['speed_at_impact_kmh'], 0.0)
        self.assertTrue(recon['was_brake_applied_prior_to_impact'])

    def test_insurance_claim_packaging(self):
        claim = InsuranceClaimsPackager.create_claim_dossier(
            incident_id=101,
            bus_number="AP16-014",
            driver_name="Ramesh Kumar",
            driver_license="AP-16-2015-1020"
        )
        self.assertEqual(claim['status'], 'DOSSIER_READY_FOR_LEGAL_FILING')
        self.assertTrue(claim['is_gps_telemetry_attached'])


if __name__ == '__main__':
    unittest.main()
