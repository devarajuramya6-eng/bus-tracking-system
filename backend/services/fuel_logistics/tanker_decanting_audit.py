"""
CityBus Enterprise Platform - Petroleum Tanker Decanting Audit & Shortage Reconciler
File: backend/services/fuel_logistics/tanker_decanting_audit.py

Reconciles bulk refinery diesel tanker deliveries into depot underground tanks:
- Invoice / Bill of Lading (Challan) volume vs ATG physical decanted volume
- Statutory allowable transit loss margin: 0.15% (Indian Oil / BPCL / HPCL norms)
- Flags suspicious shortage theft / short deliveries
"""

from typing import Dict, Any


class TankerDecantingReconciler:
    STATUTORY_TRANSIT_LOSS_TOLERANCE_PCT = 0.15

    @staticmethod
    def reconcile_decanting(challan_number: str, invoice_liters: float,
                            tank_pre_dip_liters: float, tank_post_dip_liters: float) -> Dict[str, Any]:
        """
        Reconciles received volume against delivery challan.
        """
        actual_decanted_liters = tank_post_dip_liters - tank_pre_dip_liters
        variance_liters = actual_decanted_liters - invoice_liters
        variance_pct = (variance_liters / max(1.0, invoice_liters)) * 100.0

        is_shortage_excessive = variance_pct < -TankerDecantingReconciler.STATUTORY_TRANSIT_LOSS_TOLERANCE_PCT

        return {
            'challan_number': challan_number,
            'invoice_billed_liters': round(invoice_liters, 1),
            'actual_received_liters': round(actual_decanted_liters, 1),
            'variance_liters': round(variance_liters, 1),
            'variance_percentage': round(variance_pct, 2),
            'is_short_delivery_flagged': is_shortage_excessive,
            'allowable_loss_liters': round(invoice_liters * (TankerDecantingReconciler.STATUTORY_TRANSIT_LOSS_TOLERANCE_PCT / 100.0), 1),
            'decanting_status': 'DELIVERY_ACCEPTED_WITH_SHORTAGE_CLAIM' if is_shortage_excessive else 'DECANTING_VERIFIED_CLEARED'
        }
