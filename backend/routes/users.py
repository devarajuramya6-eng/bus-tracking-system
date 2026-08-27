"""
CityBus Enterprise Platform - Users Management API
File: backend/routes/users.py

Provides full administrative and profile management for passenger, driver,
conductor, dispatcher, and administrator accounts.
"""

from flask import Blueprint, request, jsonify
from repositories.user_repository import UserRepository
from repositories.audit_repository import AuditRepository
from services.auth_service import AuthService
from models import User, db
from sqlalchemy import or_

users_bp = Blueprint('users_v1', __name__, url_prefix='/api/v1/users')


@users_bp.route('', methods=['GET'])
def get_users():
    """Lists users with filtering by role, status, search query, and pagination."""
    try:
        role = request.args.get('role')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        query = User.query
        if role and role != 'all':
            query = query.filter_by(role=role)
        if search:
            s = f"%{search}%"
            query = query.filter(or_(
                User.name.ilike(s),
                User.email.ilike(s),
                User.phone.ilike(s)
            ))

        total = query.count()
        users = query.order_by(User.id.asc()).offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "users": [u.to_dict() for u in users]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    """Fetches details for a single user."""
    try:
        user = UserRepository.get_by_id(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        return jsonify({"success": True, "user": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@users_bp.route('', methods=['POST'])
def create_user():
    """Creates a new user record with role assignment."""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        role = data.get('role', 'passenger').strip().lower()
        phone = data.get('phone', '').strip()

        if not name or not email or not password:
            return jsonify({"success": False, "message": "Name, email, and password are required"}), 400

        existing = UserRepository.get_by_email(email)
        if existing:
            return jsonify({"success": False, "message": "Email already registered"}), 409

        user = UserRepository.create_user(name, email, password, role, phone)
        AuditRepository.log_event("USER_CREATED", "User", user.id, None, request.remote_addr, f"Role: {role}")

        return jsonify({
            "success": True,
            "message": "User created successfully",
            "user": user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates user details."""
    try:
        data = request.get_json() or {}
        user = UserRepository.get_by_id(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        if 'name' in data: user.name = data['name'].strip()
        if 'phone' in data: user.phone = data['phone'].strip()
        if 'role' in data: user.role = data['role'].strip().lower()
        if 'password' in data and data['password'].strip():
            user.set_password(data['password'].strip())

        db.session.commit()
        AuditRepository.log_event("USER_UPDATED", "User", user.id, None, request.remote_addr)

        return jsonify({"success": True, "message": "User updated", "user": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user account."""
    try:
        user = UserRepository.get_by_id(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        AuditRepository.log_event("USER_DELETED", "User", user_id, None, request.remote_addr)

        return jsonify({"success": True, "message": "User deleted"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
