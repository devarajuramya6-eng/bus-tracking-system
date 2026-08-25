"""
CityBus Enterprise Platform - Transit Pass & Subscription Manager
File: backend/services/fare/pass_manager.py

Handles periodic unlimited and discounted transit passes:
- Daily Unlimited Tourist Pass (₹100)
- Monthly Metro Commuter Pass (₹1,200)
- Student Academic Semester Pass (₹600)
- Senior Citizen Silver Pass (₹800)
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import hmac
import hashlib
from config import Config


class TransitPassManager:
    PASS_PRODUCTS = {
        'DAILY_UNLIMITED': {'name': 'Daily All-Route Tourist Pass', 'price': 100.0, 'validity_days': 1},
        'MONTHLY_COMMUTER': {'name': 'Monthly Unlimited City Pass', 'price': 1200.0, 'validity_days': 30},
        'STUDENT_SEMESTER': {'name': 'Student Semester Concession Pass', 'price': 600.0, 'validity_days': 180},
        'SENIOR_SILVER': {'name': 'Senior Citizen Monthly Pass', 'price': 800.0, 'validity_days': 30}
    }

    @staticmethod
    def issue_pass(user_id: int, pass_type: str, passenger_name: str) -> Dict[str, Any]:
        """
        Issues an electronic period transit pass with cryptographic signing.
        """
        product = TransitPassManager.PASS_PRODUCTS.get(pass_type, TransitPassManager.PASS_PRODUCTS['DAILY_UNLIMITED'])
        pass_number = f"PASS-{pass_type[:3]}-{datetime.utcnow().strftime('%y%m%d')}-{user_id:04d}"
        
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(days=product['validity_days'])

        raw_payload = f"CITYBUS_PASS|{pass_number}|{user_id}|{expires_at.isoformat()}"
        signature = hmac.new(Config.SECRET_KEY.encode('utf-8'), raw_payload.encode('utf-8'), hashlib.sha256).hexdigest()[:16]

        return {
            'pass_number': pass_number,
            'user_id': user_id,
            'passenger_name': passenger_name,
            'pass_type': pass_type,
            'product_name': product['name'],
            'price_inr': product['price'],
            'issued_at': issued_at.isoformat(),
            'expires_at': expires_at.isoformat(),
            'status': 'ACTIVE',
            'qr_payload': f"{raw_payload}|{signature}"
        }
