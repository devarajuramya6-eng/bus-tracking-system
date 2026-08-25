import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Float, Date, Enum
from sqlalchemy.orm import relationship
import enum

try:
    from backend.database import Base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

class RevenueSource(str, enum.Enum):
    TICKET_SALES = "TICKET_SALES"
    PASS_SUBSCRIPTIONS = "PASS_SUBSCRIPTIONS"
    PENALTIES = "PENALTIES"
    ADVERTISEMENTS = "ADVERTISEMENTS"
    CHARTER_SERVICES = "CHARTER_SERVICES"
    OTHER = "OTHER"

class PaymentMethodAggregation(str, enum.Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    MOBILE_WALLET = "MOBILE_WALLET"
    CASH = "CASH"
    TRANSIT_CARD = "TRANSIT_CARD"
    VOUCHER = "VOUCHER"

class DailyRevenueAnalytics(Base):
    """
    Aggregated daily revenue analytics for reporting and dashboarding.
    Pre-calculated nightly to ensure dashboard queries are lightning fast.
    """
    __tablename__ = "daily_revenue_analytics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    report_date = Column(Date, nullable=False, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # High-level metrics
    total_revenue = Column(Float, nullable=False, default=0.0)
    total_transactions = Column(Integer, nullable=False, default=0)
    average_transaction_value = Column(Float, nullable=False, default=0.0)
    refunded_amount = Column(Float, nullable=False, default=0.0)
    net_revenue = Column(Float, nullable=False, default=0.0)
    
    # Granular Revenue Breakdown (JSON objects for flexibility)
    revenue_by_source = Column(JSON, nullable=False, default=lambda: {}) # e.g., {"TICKET_SALES": 5000, "PASS_SUBSCRIPTIONS": 2000}
    revenue_by_payment_method = Column(JSON, nullable=False, default=lambda: {}) # e.g., {"CREDIT_CARD": 4000, "CASH": 1000}
    revenue_by_route = Column(JSON, nullable=False, default=lambda: {}) # Route ID to revenue mapping
    revenue_by_ticket_type = Column(JSON, nullable=False, default=lambda: {}) # e.g., {"SINGLE_RIDE": 3000, "DAY_PASS": 1500}
    
    # Peak Analysis
    peak_revenue_hour = Column(Integer, nullable=True) # 0-23
    peak_revenue_amount = Column(Float, nullable=True)
    
    # Performance against targets
    target_revenue = Column(Float, nullable=True)
    variance_percentage = Column(Float, nullable=True) # positive means above target, negative means below

    def __repr__(self):
        return f"<DailyRevenueAnalytics {self.report_date} - Net: {self.net_revenue}>"

    def to_dict(self):
        return {
            "id": self.id,
            "report_date": self.report_date.isoformat(),
            "total_revenue": self.total_revenue,
            "total_transactions": self.total_transactions,
            "average_transaction_value": self.average_transaction_value,
            "refunded_amount": self.refunded_amount,
            "net_revenue": self.net_revenue,
            "revenue_by_source": self.revenue_by_source,
            "revenue_by_payment_method": self.revenue_by_payment_method,
            "revenue_by_route": self.revenue_by_route,
            "peak_revenue_hour": self.peak_revenue_hour,
            "target_revenue": self.target_revenue,
            "variance_percentage": self.variance_percentage
        }
