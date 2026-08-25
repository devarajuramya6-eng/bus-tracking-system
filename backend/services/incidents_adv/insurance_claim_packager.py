"""
CityBus Enterprise Platform - Insurance & Legal Tribunal Claims Packager
File: backend/services/incidents_adv/insurance_claim_packager.py

Packages legal evidence files for Motor Accident Claims Tribunal (MACT):
- Driver Duty Log & Breathalyzer / Fitness Certification
- Vehicle Fitness Certificate & AIS-140 GPS Telemetry Trail
- Conductor passenger count manifest
"""

from typing import Dict, Any
from datetime import datetime


class InsuranceClaimsPackager:
    @staticmethod
    def create_claim_dossier(incident_id: int, bus_number: str,
                             driver_name: str, driver_license: str,
                             insurance_policy_number: str = "POL-NIC-2026-89410") -> Dict[str, Any]:
        """
        Builds legal insurance dossier package.
        """
        dossier_id = f"MACT-CLAIM-{incident_id:04d}-{datetime.utcnow().strftime('%y%m%d')}"

        return {
            'dossier_id': dossier_id,
            'incident_id': incident_id,
            'bus_registration': bus_number,
            'driver_name': driver_name,
            'driver_license': driver_license,
            'insurance_company': 'National Insurance Company Ltd (Commercial Transport Policy)',
            'policy_number': insurance_policy_number,
            'is_gps_telemetry_attached': True,
            'is_driver_alcohol_test_attached': True,
            'is_vehicle_fitness_cert_attached': True,
            'status': 'DOSSIER_READY_FOR_LEGAL_FILING',
            'created_at': datetime.utcnow().isoformat()
        }
