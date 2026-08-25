"""
CityBus Enterprise Platform - Authentication API Routes
File: backend/routes/auth.py
"""

from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from repositories.user_repository import UserRepository

auth_bp = Blueprint('auth_v1', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticates users across all 9 roles and returns JWT access + refresh tokens."""
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        ip = request.remote_addr
        tokens, err = AuthService.authenticate(email, password, ip)
        if err:
            return jsonify({"success": False, "message": err}), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            **tokens
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registers a new passenger user."""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        phone = data.get('phone', '').strip()
        role = data.get('role', 'passenger').strip().lower()

        if not name or not email or not password:
            return jsonify({"success": False, "message": "Name, email, and password are required"}), 400

        existing = UserRepository.get_by_email(email)
        if existing:
            return jsonify({"success": False, "message": "An account with this email already exists"}), 409

        user = UserRepository.create_user(name, email, password, role, phone)
        tokens = AuthService.generate_tokens(user)

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            **tokens
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refreshes expired access token using valid refresh token."""
    try:
        data = request.get_json() or {}
        refresh_token = data.get('refresh_token')
        if not refresh_token:
            return jsonify({"success": False, "message": "Refresh token is required"}), 400

        tokens, err = AuthService.refresh_access_token(refresh_token)
        if err:
            return jsonify({"success": False, "message": err}), 401

        return jsonify({
            "success": True,
            **tokens
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Returns profile for currently authenticated user."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"success": False, "message": "Missing Bearer token"}), 401

    token = auth_header.split(' ')[1]
    payload = AuthService.verify_token(token)
    if not payload:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 401

    user = UserRepository.get_by_id(payload['sub'])
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 200
