"""
CityBus Enterprise Platform - Concession Document Verification Engine
File: backend/services/afc/concession_document_ocr.py

Automates student ID card and senior citizen Aadhaar identity verification:
- College enrollment validation & expiration check
- Senior citizen age threshold calculation (Age >= 60)
- Disability certificate registration format validation
"""

from datetime import datetime
from typing import Dict, Any


class ConcessionDocumentVerifier:
    @staticmethod
    def verify_student_document(institution_name: str, roll_number: str, academic_year_end: int) -> Dict[str, Any]:
        """
        Validates college student concession eligibility.
        """
        current_year = datetime.utcnow().year
        is_valid_year = academic_year_end >= current_year
        has_valid_roll = len(roll_number.strip()) >= 5

        is_eligible = is_valid_year and has_valid_roll

        return {
            'institution_name': institution_name,
            'roll_number': roll_number,
            'academic_valid_until_year': academic_year_end,
            'is_eligible': is_eligible,
            'concession_category': 'STUDENT_50_PCT',
            'status': 'APPROVED' if is_eligible else 'REJECTED_EXPIRED_ENROLLMENT'
        }

    @staticmethod
    def verify_senior_citizen_document(aadhaar_last_four: str, birth_year: int) -> Dict[str, Any]:
        """
        Validates senior citizen age eligibility (Age >= 60).
        """
        current_year = datetime.utcnow().year
        age = current_year - birth_year
        is_eligible = age >= 60 and len(aadhaar_last_four.strip()) == 4

        return {
            'aadhaar_masked': f"XXXX-XXXX-{aadhaar_last_four}",
            'calculated_age': age,
            'is_eligible': is_eligible,
            'concession_category': 'SENIOR_CITIZEN_30_PCT',
            'status': 'APPROVED' if is_eligible else 'REJECTED_UNDERAGE'
        }
