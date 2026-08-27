"""
CityBus Enterprise Platform - Conductor Repository
File: backend/repositories/conductor_repository.py

Encapsulates data access and operations for Conductor profiles,
ticket validation metrics, shift manifests, and cash collections.
"""

from datetime import datetime
from models import db, Conductor, Bus, Ticket, Trip
from sqlalchemy import or_


class ConductorRepository:
    """Data access layer for transit fare conductors."""

    @staticmethod
    def get_all(status=None, search=None, page=1, per_page=20):
        """Retrieves conductors with pagination and filtering."""
        query = Conductor.query
        if status and status != 'all':
            query = query.filter_by(status=status)
        if search:
            s = f"%{search}%"
            query = query.filter(or_(
                Conductor.name.ilike(s),
                Conductor.phone.ilike(s),
                Conductor.badge_id.ilike(s)
            ))
        
        total = query.count()
        conductors = query.order_by(Conductor.id.asc()).offset((page - 1) * per_page).limit(per_page).all()
        return conductors, total

    @staticmethod
    def get_by_id(conductor_id):
        """Fetches conductor by ID."""
        return Conductor.query.get(conductor_id)

    @staticmethod
    def create(name, phone, badge_id, status='Active'):
        """Creates a new conductor profile."""
        conductor = Conductor(
            name=name.strip(),
            phone=phone.strip(),
            badge_id=badge_id.strip(),
            status=status
        )
        db.session.add(conductor)
        db.session.commit()
        return conductor

    @staticmethod
    def update(conductor_id, **kwargs):
        """Updates conductor attributes."""
        conductor = Conductor.query.get(conductor_id)
        if not conductor:
            return None
        for key, val in kwargs.items():
            if hasattr(conductor, key) and key != 'id':
                setattr(conductor, key, val)
        db.session.commit()
        return conductor

    @staticmethod
    def delete(conductor_id):
        """Deletes conductor profile if unassigned."""
        conductor = Conductor.query.get(conductor_id)
        if not conductor:
            return False, "Conductor not found"
        
        # Clear bus assignments
        buses = Bus.query.filter_by(conductor_id=conductor_id).all()
        for b in buses:
            b.conductor_id = None
            
        db.session.delete(conductor)
        db.session.commit()
        return True, None

    @staticmethod
    def get_validation_summary(conductor_id, date_str=None):
        """Calculates ticket verification counts and total revenue collected."""
        conductor = Conductor.query.get(conductor_id)
        if not conductor:
            return None
            
        # Get active bus
        assigned_bus = Bus.query.filter_by(conductor_id=conductor_id).first()
        bus_id = assigned_bus.id if assigned_bus else None
        
        query = Ticket.query
        if bus_id:
            query = query.filter_by(bus_id=bus_id)
            
        total_tickets = query.count()
        used_tickets = query.filter_by(status='USED').count()
        valid_tickets = query.filter_by(status='VALID').count()
        
        # Calculate revenue
        used_records = query.filter_by(status='USED').all()
        total_revenue = sum(t.fare_amount for t in used_records)
        
        return {
            "conductor_id": conductor.id,
            "name": conductor.name,
            "badge_id": conductor.badge_id,
            "status": conductor.status,
            "assigned_bus": assigned_bus.to_dict() if assigned_bus else None,
            "total_tickets_handled": total_tickets,
            "scanned_tickets_count": used_tickets,
            "active_valid_tickets": valid_tickets,
            "total_revenue_inr": round(total_revenue, 2)
        }
