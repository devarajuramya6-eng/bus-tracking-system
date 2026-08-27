"""
CityBus Enterprise Platform - Notification Repository
File: backend/repositories/notification_repository.py

Encapsulates user alerts, push messages, unread status tracking,
and notification preference configurations.
"""

from datetime import datetime
from models import db, Notification
from sqlalchemy import desc


class NotificationRepository:
    """Data access layer for system & passenger notifications."""

    @staticmethod
    def get_by_user(user_id, unread_only=False, page=1, per_page=20):
        """Retrieves notifications for a specific user ID."""
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
            
        total = query.count()
        notifications = query.order_by(Notification.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return notifications, total

    @staticmethod
    def get_unread_count(user_id):
        """Returns the number of unread notifications for user."""
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def create(user_id, title, message, category='system', action_url=None):
        """Creates and stores a new notification record."""
        notification = Notification(
            user_id=user_id,
            title=title.strip(),
            message=message.strip(),
            category=category,
            action_url=action_url,
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
        return notification

    @staticmethod
    def mark_as_read(notification_id, user_id=None):
        """Marks a single notification as read."""
        query = Notification.query.filter_by(id=notification_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        notif = query.first()
        if notif:
            notif.is_read = True
            db.session.commit()
            return notif
        return None

    @staticmethod
    def mark_all_as_read(user_id):
        """Marks all unread notifications for a user as read."""
        updated = Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
        db.session.commit()
        return updated

    @staticmethod
    def delete(notification_id, user_id=None):
        """Deletes a notification."""
        query = Notification.query.filter_by(id=notification_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        notif = query.first()
        if notif:
            db.session.delete(notif)
            db.session.commit()
            return True
        return False
