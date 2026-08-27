"""
CityBus Enterprise Platform - Notification Service
File: backend/services/notification_service.py

Dispatches real-time user push notifications, transit disruption warnings,
trip delay advisories, and digital ticket purchase receipts.
"""

from typing import Dict, List, Any, Optional
from repositories.notification_repository import NotificationRepository
from repositories.user_repository import UserRepository
from models import Notification, User, db
from websocket.socket_manager import socketio, HAS_SOCKETIO


class NotificationService:
    """Business logic for omnichannel passenger and staff notifications."""

    @staticmethod
    def send_notification(user_id: int, title: str, message: str, category: str = "system", action_url: Optional[str] = None) -> Dict[str, Any]:
        """Creates a persistent notification and emits WebSocket event to active user session."""
        notif = NotificationRepository.create(user_id, title, message, category, action_url)
        notif_dict = notif.to_dict()

        # Emit real-time WebSocket push if user is connected
        if HAS_SOCKETIO:
            try:
                socketio.emit('notification:new', notif_dict, room=f"user:{user_id}")
            except Exception:
                pass

        return notif_dict

    @staticmethod
    def broadcast_to_role(role: str, title: str, message: str, category: str = "broadcast") -> int:
        """Broadcasts a notification to all users holding a specific role."""
        users = User.query.filter_by(role=role).all()
        count = 0
        for u in users:
            NotificationService.send_notification(u.id, title, message, category)
            count += 1
        return count

    @staticmethod
    def broadcast_system_alert(title: str, message: str) -> int:
        """Broadcasts a high-priority advisory to all registered users."""
        users = User.query.all()
        count = 0
        for u in users:
            NotificationService.send_notification(u.id, title, message, category="emergency")
            count += 1
            
        if HAS_SOCKETIO:
            try:
                socketio.emit('alert:system_broadcast', {
                    "title": title,
                    "message": message,
                    "severity": "High"
                }, broadcast=True)
            except Exception:
                pass

        return count

    @staticmethod
    def send_ticket_receipt(user_id: int, ticket_number: str, route_name: str, fare: float) -> Dict[str, Any]:
        """Generates an instant in-app purchase confirmation notification."""
        title = "Ticket Confirmed"
        message = f"Your digital ticket #{ticket_number} for {route_name} (₹{fare:.2f}) is ready in your wallet."
        return NotificationService.send_notification(user_id, title, message, category="ticket", action_url="/my-tickets.html")

    @staticmethod
    def send_delay_alert(user_id: int, bus_number: str, delay_minutes: int) -> Dict[str, Any]:
        """Notifies a passenger about approaching bus delay."""
        title = f"Bus {bus_number} Delayed"
        message = f"Your bus {bus_number} is experiencing a {delay_minutes}-minute delay due to traffic."
        return NotificationService.send_notification(user_id, title, message, category="delay")
