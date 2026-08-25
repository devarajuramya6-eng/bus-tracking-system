"""
CityBus Enterprise Platform - Base Database Setup & Model Mixin
File: backend/models/base.py
"""

from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModelMixin:
    """Base mixin providing timestamps and automatic dictionary serialization."""
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Standard JSON serialization."""
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if isinstance(val, datetime):
                result[column.name] = val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(val, (int, float, str, bool)) or val is None:
                result[column.name] = val
            else:
                try:
                    result[column.name] = json.loads(val)
                except:
                    result[column.name] = str(val)
        return result

    def save(self):
        """Commits model changes to database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Deletes model instance from database."""
        db.session.delete(self)
        db.session.commit()
