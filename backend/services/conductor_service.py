"""
CityBus Enterprise Platform - Conductor & Ticketing Remittance Service
File: backend/services/conductor_service.py

Orchestrates electronic ticket inspection, on-board cash ticket issuance,
passenger boarding counts, and end-of-shift fare box reconciliation.
"""

from typing import Dict, List, Any, Optional, Tuple
from repositories.conductor_repository import ConductorRepository
from repositories.ticket_repository import TicketRepository
from repositories.audit_repository import AuditRepository
from models import Conductor, Ticket, Bus, db


class ConductorService:
    """Business logic for on-board fare collection and ticket validation."""

    @staticmethod
    def get_conductor_dashboard(conductor_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Retrieves real-time stats for the conductor mobile terminal."""
        conductor = ConductorRepository.get_by_id(conductor_id)
        if not conductor:
            return None, "Conductor not found"

        summary = ConductorRepository.get_validation_summary(conductor_id)
        return {
            "conductor": conductor.to_dict(),
            "summary": summary
        }, None

    @staticmethod
    def validate_ticket(qr_payload: str, bus_id: Optional[int] = None) -> Dict[str, Any]:
        """Cryptographically verifies QR payload, prevents replay attacks, and marks ticket as USED."""
        ticket, err = TicketRepository.validate_qr(qr_payload)
        if err:
            return {
                "success": False,
                "status": "INVALID",
                "message": err
            }

        AuditRepository.log_event("TICKET_SCANNED_VALID", "Ticket", ticket.id, None, None, f"Bus: {bus_id}")
        return {
            "success": True,
            "status": "VALID",
            "message": "Ticket verified successfully",
            "ticket": ticket.to_dict()
        }
