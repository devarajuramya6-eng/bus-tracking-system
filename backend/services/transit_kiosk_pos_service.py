"""
CityBus Enterprise Platform - Self-Service Transit Kiosk POS Service
File: backend/services/transit_kiosk_pos_service.py

Governs physical touch-screen ticketing vending machines (TVM) at major stations (PNBS, Benz Circle, Airport):
- Cash bill validator & coins dispenser state machine
- Thermal paper receipt printing & QR encoding
- Instant UPI QR display on customer-facing display (CFD)
"""

import time
from typing import Dict, List, Any, Optional
from models import Ticket, db
from repositories.audit_repository import AuditRepository


class TransitKioskPOSService:
    """Manages unattended ticket vending machines (TVMs) at bus station platforms."""

    _kiosks: Dict[str, Dict[str, Any]] = {
        "TVM-PNBS-01": {"name": "PNBS Terminal Platform 1 Kiosk", "paper_roll_pct": 82, "cash_box_inr": 14500, "status": "ONLINE"},
        "TVM-PNBS-02": {"name": "PNBS Terminal Platform 4 Kiosk", "paper_roll_pct": 64, "cash_box_inr": 8900, "status": "ONLINE"},
        "TVM-BENZ-01": {"name": "Benz Circle Main Shelter Kiosk", "paper_roll_pct": 95, "cash_box_inr": 5200, "status": "ONLINE"},
        "TVM-AIRPORT-01": {"name": "Gannavaram Airport Arrival Kiosk", "paper_roll_pct": 88, "cash_box_inr": 12000, "status": "ONLINE"}
    }

    @classmethod
    def get_kiosk_status(cls, kiosk_id: str) -> Optional[Dict[str, Any]]:
        """Returns hardware health metrics for a TVM unit."""
        return cls._kiosks.get(kiosk_id)

    @classmethod
    def issue_kiosk_ticket(cls, kiosk_id: str, route_id: int, origin_stop: str, dest_stop: str,
                           fare_amount: float, payment_method: str = "UPI") -> Dict[str, Any]:
        """Processes transaction at kiosk terminal and dispenses ticket."""
        kiosk = cls._kiosks.get(kiosk_id, {"name": "General Station Kiosk"})
        txn_id = f"TVM-{int(time.time()*1000)}"

        # Consume thermal paper (0.1% per print)
        if kiosk_id in cls._kiosks:
            cls._kiosks[kiosk_id]["paper_roll_pct"] = max(0, cls._kiosks[kiosk_id]["paper_roll_pct"] - 1)
            if payment_method == "CASH":
                cls._kiosks[kiosk_id]["cash_box_inr"] += int(fare_amount)

        AuditRepository.log_event("KIOSK_TICKET_DISPENSED", "KioskPOS", txn_id, None, None, f"Kiosk: {kiosk_id}, Fare: ₹{fare_amount}")

        return {
            "transaction_id": txn_id,
            "kiosk_id": kiosk_id,
            "origin_stop": origin_stop,
            "destination_stop": dest_stop,
            "fare_paid_inr": fare_amount,
            "payment_method": payment_method,
            "qr_code_payload": f"QR-TVM-{txn_id}-{int(fare_amount)}",
            "printed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
