import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
import enum

try:
    from backend.database import Base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

class ActionType(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    REPORT_GENERATION = "REPORT_GENERATION"
    MAINTENANCE_LOG = "MAINTENANCE_LOG"
    SECURITY_ALERT = "SECURITY_ALERT"
    SYSTEM_CONFIG_CHANGE = "SYSTEM_CONFIG_CHANGE"

class AuditSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AuditLog(Base):
    """
    Comprehensive Audit Logging for all system actions.
    Ensures that every action taken by an admin, dispatcher, or driver is tracked
    for compliance and security purposes.
    """
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    actor_id = Column(String(36), nullable=True, index=True) # removed foreign key to avoid dependency issues if User model is different
    actor_role = Column(String(50), nullable=True) # E.g., 'Admin', 'Dispatcher', 'Driver'
    
    action_type = Column(Enum(ActionType), nullable=False, index=True)
    severity = Column(Enum(AuditSeverity), default=AuditSeverity.LOW)
    
    resource_type = Column(String(100), nullable=False, index=True) # E.g., 'Bus', 'Route', 'User'
    resource_id = Column(String(36), nullable=True, index=True)
    
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    # Optional detailed message or context
    context = Column(String(1000), nullable=True)

    def __repr__(self):
        return f"<AuditLog {self.action_type.value} on {self.resource_type} by {self.actor_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "actor_id": self.actor_id,
            "actor_role": self.actor_role,
            "action_type": self.action_type.value,
            "severity": self.severity.value,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "context": self.context
        }
