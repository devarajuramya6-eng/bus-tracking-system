"""
CityBus Enterprise Platform - Maintenance Repository
File: backend/repositories/maintenance_repository.py

Encapsulates vehicle repair work orders, scheduled PM inspections,
depot servicing, and technician assignments.
"""

from datetime import datetime
from models import db, MaintenanceWorkOrder, Bus
from sqlalchemy import or_, desc


class MaintenanceRepository:
    """Data access layer for depot vehicle maintenance operations."""

    @staticmethod
    def get_all(status=None, bus_id=None, priority=None, page=1, per_page=20):
        """Retrieves maintenance work orders with filtering and pagination."""
        query = MaintenanceWorkOrder.query
        
        if status and status != 'all':
            query = query.filter_by(status=status)
        if bus_id:
            query = query.filter_by(bus_id=bus_id)
        if priority:
            query = query.filter_by(priority=priority)
            
        total = query.count()
        orders = query.order_by(MaintenanceWorkOrder.scheduled_date.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return orders, total

    @staticmethod
    def get_by_id(order_id):
        """Fetches work order by primary key ID."""
        return MaintenanceWorkOrder.query.get(order_id)

    @staticmethod
    def create(bus_id, issue_description, priority="Normal", technician_name=None, cost_estimate=0.0, scheduled_date=None):
        """Creates a new maintenance work order."""
        order = MaintenanceWorkOrder(
            bus_id=bus_id,
            issue_description=issue_description.strip(),
            priority=priority,
            technician_name=technician_name.strip() if technician_name else "Depot Tech Team",
            cost_estimate=cost_estimate,
            status="OPEN",
            scheduled_date=scheduled_date or datetime.utcnow()
        )
        db.session.add(order)
        
        # Update bus status to Maintenance if High or Critical priority
        if priority in ["High", "Critical"]:
            bus = Bus.query.get(bus_id)
            if bus:
                bus.status = "Maintenance"
                
        db.session.commit()
        return order

    @staticmethod
    def update(order_id, **kwargs):
        """Updates work order details and state machine."""
        order = MaintenanceWorkOrder.query.get(order_id)
        if not order:
            return None
            
        for key, val in kwargs.items():
            if hasattr(order, key) and key != 'id':
                setattr(order, key, val)
                
        # If work order is closed, restore bus status if offline/maintenance
        if kwargs.get('status') == 'CLOSED':
            order.completion_date = datetime.utcnow()
            bus = Bus.query.get(order.bus_id)
            if bus and bus.status == 'Maintenance':
                bus.status = 'Offline'
                
        db.session.commit()
        return order

    @staticmethod
    def delete(order_id):
        """Deletes a work order."""
        order = MaintenanceWorkOrder.query.get(order_id)
        if not order:
            return False
        db.session.delete(order)
        db.session.commit()
        return True
