"""
CityBus Enterprise Platform - Maintenance & Depot Workshop Service
File: backend/services/maintenance_service.py

Orchestrates vehicle preventive maintenance, technician task assignment,
spare parts stock requisition, and vehicle status restoration.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from repositories.maintenance_repository import MaintenanceRepository
from repositories.bus_repository import BusRepository
from repositories.audit_repository import AuditRepository
from models import MaintenanceWorkOrder, Bus, db


class MaintenanceService:
    """Coordinates workshop work orders and vehicle roadworthiness inspection."""

    @staticmethod
    def get_maintenance_overview() -> Dict[str, Any]:
        """Calculates depot repair workload and vehicle breakdown ratios."""
        orders, total = MaintenanceRepository.get_all(page=1, per_page=100)
        open_orders = [o for o in orders if o.status == 'OPEN']
        in_progress = [o for o in orders if o.status == 'IN_PROGRESS']
        closed = [o for o in orders if o.status == 'CLOSED']

        total_cost = sum(o.cost_estimate or 0.0 for o in orders)

        return {
            "total_work_orders": total,
            "open_work_orders": len(open_orders),
            "in_progress_orders": len(in_progress),
            "completed_orders": len(closed),
            "total_maintenance_expenditure_inr": round(total_cost, 2),
            "recent_orders": [o.to_dict() for o in orders[:10]]
        }

    @staticmethod
    def create_work_order(bus_id: int, issue_description: str, priority: str = "Normal",
                          technician_name: Optional[str] = None, cost_estimate: float = 0.0) -> Dict[str, Any]:
        """Creates a maintenance ticket and logs audit trail."""
        order = MaintenanceRepository.create(
            bus_id=bus_id,
            issue_description=issue_description,
            priority=priority,
            technician_name=technician_name,
            cost_estimate=cost_estimate
        )
        AuditRepository.log_event("MAINTENANCE_ORDER_CREATED", "MaintenanceWorkOrder", order.id, None, None, f"Bus ID: {bus_id}")
        return order.to_dict()

    @staticmethod
    def complete_work_order(order_id: int, notes: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Closes a work order and restores vehicle operational readiness."""
        order = MaintenanceRepository.update(
            order_id,
            status='CLOSED',
            completion_date=datetime.utcnow()
        )
        if not order:
            return None, "Work order not found"

        AuditRepository.log_event("MAINTENANCE_ORDER_CLOSED", "MaintenanceWorkOrder", order_id, None, None)
        return order.to_dict(), None
