"""
CityBus Enterprise Platform - Authentication & RBAC Service
File: backend/services/auth_service.py
"""

import time
import json
import base64
import hmac
import hashlib
from config import Config
from repositories.user_repository import UserRepository

try:
    import jwt
    HAS_PYJWT = True
except ImportError:
    HAS_PYJWT = False


class AuthService:
    """Handles JWT generation, verification, password checking, and role permissions."""

    @staticmethod
    def generate_tokens(user):
        """Generates Access Token (8 hours) and Refresh Token (30 days)."""
        now = int(time.time())
        
        access_payload = {
            'sub': str(user.id),
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'iat': now,
            'exp': now + int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            'type': 'access'
        }
        
        refresh_payload = {
            'sub': str(user.id),
            'iat': now,
            'exp': now + int(Config.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
            'type': 'refresh'
        }

        if HAS_PYJWT:
            access_token = jwt.encode(access_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
            refresh_token = jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
            if isinstance(access_token, bytes):
                access_token = access_token.decode('utf-8')
            if isinstance(refresh_token, bytes):
                refresh_token = refresh_token.decode('utf-8')
        else:
            # Standalone HMAC-SHA256 JWT Generator
            access_token = AuthService._custom_jwt_encode(access_payload)
            refresh_token = AuthService._custom_jwt_encode(refresh_payload)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            'user': user.to_dict()
        }

    @staticmethod
    def _custom_jwt_encode(payload):
        header = {"alg": "HS256", "typ": "JWT"}
        h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').rstrip('=')
        p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').rstrip('=')
        sig_data = f"{h_b64}.{p_b64}"
        sig = hmac.new(Config.SECRET_KEY.encode('utf-8'), sig_data.encode('utf-8'), hashlib.sha256).digest()
        s_b64 = base64.urlsafe_b64encode(sig).decode('utf-8').rstrip('=')
        return f"{h_b64}.{p_b64}.{s_b64}"

    @staticmethod
    def _custom_jwt_decode(token):
        parts = token.split('.')
        if len(parts) != 3:
            return None
        h_b64, p_b64, s_b64 = parts
        sig_data = f"{h_b64}.{p_b64}"
        expected_sig = hmac.new(Config.SECRET_KEY.encode('utf-8'), sig_data.encode('utf-8'), hashlib.sha256).digest()
        expected_s_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')
        if not hmac.compare_digest(s_b64, expected_s_b64):
            return None
        
        # Add padding back
        pad = len(p_b64) % 4
        if pad:
            p_b64 += '=' * (4 - pad)
        data = json.loads(base64.urlsafe_b64decode(p_b64.encode('utf-8')).decode('utf-8'))
        if 'exp' in data and time.time() > data['exp']:
            return None
        return data

    @staticmethod
    def verify_token(token):
        """Verifies JWT token validity and returns decoded payload."""
        if not token:
            return None
        if HAS_PYJWT:
            try:
                return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            except Exception:
                pass
        return AuthService._custom_jwt_decode(token)

    @staticmethod
    def authenticate(email, password, ip=None):
        """Validates credentials and returns JWT tokens."""
        user = UserRepository.get_by_email(email)
        if not user or not user.check_password(password):
            return None, "Invalid email or password"

        if not user.is_active:
            return None, "User account is suspended. Contact administrator."

        UserRepository.log_audit("USER_LOGIN", "User", user.id, f"User {user.email} logged in", user.id, user.email, ip)
        tokens = AuthService.generate_tokens(user)
        return tokens, None

    @staticmethod
    def refresh_access_token(refresh_token):
        """Generates a new access token from a valid refresh token."""
        payload = AuthService.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return None, "Invalid or expired refresh token"

        user = UserRepository.get_by_id(payload['sub'])
        if not user or not user.is_active:
            return None, "User not found or inactive"

        tokens = AuthService.generate_tokens(user)
        return tokens, None
