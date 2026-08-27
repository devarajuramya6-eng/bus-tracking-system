"""
CityBus Enterprise Platform - Notifications API
File: backend/routes/notifications.py

Handles user alerts, dispatch broadcasts, unread badge counters,
and notification read state transitions.
"""

from flask import Blueprint, request, jsonify
from repositories.notification_repository import NotificationRepository
from services.auth_service import AuthService
from models import Notification, db

notifications_bp = Blueprint('notifications_v1', __name__, url_prefix='/api/v1/notifications')


@notifications_bp.route('', methods=['GET'])
def get_user_notifications():
    """Retrieves notifications for the currently authenticated user or user_id query."""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        notifications, total = NotificationRepository.get_by_user(user_id, unread_only, page, per_page)
        unread_count = NotificationRepository.get_unread_count(user_id)

        return jsonify({
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "unread_count": unread_count,
            "notifications": [n.to_dict() for n in notifications]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@notifications_bp.route('/unread-count', methods=['GET'])
def get_unread_badge_count():
    """Returns the unread count for UI badges."""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        unread_count = NotificationRepository.get_unread_count(user_id)
        return jsonify({"success": True, "unread_count": unread_count}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@notifications_bp.route('/<int:notification_id>/read', methods=['POST', 'PUT'])
def mark_single_read(notification_id):
    """Marks a single notification as read."""
    try:
        user_id = request.args.get('user_id', type=int)
        notif = NotificationRepository.mark_as_read(notification_id, user_id)
        if not notif:
            return jsonify({"success": False, "message": "Notification not found"}), 404
        return jsonify({"success": True, "notification": notif.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@notifications_bp.route('/read-all', methods=['POST', 'PUT'])
def mark_all_notifications_read():
    """Marks all notifications as read for a user."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id') or request.args.get('user_id', 1, type=int)
        count = NotificationRepository.mark_all_as_read(user_id)
        return jsonify({"success": True, "marked_count": count}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@notifications_bp.route('', methods=['POST'])
def send_notification():
    """Creates a notification for a user (used by admin or system services)."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        category = data.get('category', 'system')
        action_url = data.get('action_url')

        if not user_id or not title or not message:
            return jsonify({"success": False, "message": "user_id, title, and message are required"}), 400

        notif = NotificationRepository.create(user_id, title, message, category, action_url)
        return jsonify({"success": True, "notification": notif.to_dict()}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
