"""
CityBus Enterprise Platform - User Repository
File: backend/repositories/user_repository.py
"""

from models import db, User, Driver, Conductor, AuditLog


class UserRepository:
    """Isolates database queries for Users, Drivers, Conductors, and Audit Logs."""

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter(User.email.ilike(email.strip())).first()

    @staticmethod
    def create_user(name, email, password, role="passenger", phone=None):
        user = User(name=name, email=email.strip().lower(), role=role, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_drivers():
        return Driver.query.all()

    @staticmethod
    def get_all_conductors():
        return Conductor.query.all()

    @staticmethod
    def log_audit(action, entity_type, entity_id=None, details="", user_id=None, user_email=None, ip=None):
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            details=details,
            user_id=user_id,
            user_email=user_email,
            ip_address=ip
        )
        db.session.add(log)
        db.session.commit()
        return log
