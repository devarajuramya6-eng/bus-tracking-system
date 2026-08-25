"""
CityBus Enterprise Platform - User Model
File: backend/models/user.py
"""

from datetime import datetime
import hashlib
from models.base import db, BaseModelMixin


class User(db.Model, BaseModelMixin):
    """User account entity with password hashing, RBAC role, and profile."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    role = db.Column(db.String(50), default="passenger", nullable=False, index=True)
    # Roles: passenger, driver, conductor, dispatcher, fleet_manager, maintenance_manager, finance_manager, admin, super_admin
    avatar_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    tickets = db.relationship('Ticket', backref='user_rel', lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship('Favorite', backref='user_rel', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='user_rel', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hashes password using SHA-256 with salt."""
        salt = "citybus_salt_2026_"
        self.password_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

    def check_password(self, password):
        """Verifies plaintext password against stored hash."""
        salt = "citybus_salt_2026_"
        hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return self.password_hash == hashed or self.password_hash == password  # backward compatible with plain demo passwords

    def to_dict(self):
        data = super().to_dict()
        data.pop('password_hash', None)
        return data
