"""
CityBus Enterprise Platform - Central Workshop Bay & Job Card Scheduler
File: backend/services/maintenance_ops/workshop_scheduler.py

Allocates depot repair bays and assigns specialized technician mechanics:
- Specialized Bay Types: UNDERBODY_PIT, HYDRAULIC_LIFT, EV_BATTERY_DIAGNOSTIC, PAINT_BODY
- Priority queuing for roadside breakdown pull-ins vs scheduled periodic A/B/C checks
"""

from typing import List, Dict, Any


class WorkshopBayScheduler:
    WORKSHOP_BAYS = [
        {'bay_id': 'BAY-PIT-01', 'type': 'UNDERBODY_PIT', 'status': 'OCCUPIED', 'assigned_bus': 'AP16-004', 'job': 'Brake Pad Overhaul', 'lead_mechanic': 'K. Satyanarayana'},
        {'bay_id': 'BAY-PIT-02', 'type': 'UNDERBODY_PIT', 'status': 'AVAILABLE', 'assigned_bus': None, 'job': None, 'lead_mechanic': None},
        {'bay_id': 'BAY-LFT-01', 'type': 'HYDRAULIC_LIFT', 'status': 'OCCUPIED', 'assigned_bus': 'AP16-012', 'job': 'Transmission Fluid Service', 'lead_mechanic': 'M. Venkatesh'},
        {'bay_id': 'BAY-EV-01', 'type': 'EV_BATTERY_DIAGNOSTIC', 'status': 'AVAILABLE', 'assigned_bus': None, 'job': None, 'lead_mechanic': None},
        {'bay_id': 'BAY-PNT-01', 'type': 'PAINT_BODY', 'status': 'OCCUPIED', 'assigned_bus': 'AP16-027', 'job': 'Side Fender Dent Repair', 'lead_mechanic': 'S. Raju'}
    ]

    @staticmethod
    def get_workshop_overview() -> Dict[str, Any]:
        bays = WorkshopBayScheduler.WORKSHOP_BAYS
        occupied = sum(1 for b in bays if b['status'] == 'OCCUPIED')
        available = len(bays) - occupied

        return {
            'depot_facility': 'Autonagar Central Heavy Maintenance Facility',
            'total_bays': len(bays),
            'occupied_bays': occupied,
            'available_bays': available,
            'utilization_pct': round((occupied / len(bays)) * 100.0, 1),
            'bays': bays
        }
