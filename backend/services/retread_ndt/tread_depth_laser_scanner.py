"""
CityBus Enterprise Platform - Drive-Over In-Ground Tread Depth Laser Scanner
File: backend/services/retread_ndt/tread_depth_laser_scanner.py

Processes in-ground depot drive-over optical laser triangulation scanners:
- Measures 3D groove depth across Steer (Axle 1: Left/Right) and Dual Drive (Axle 2: 4 Tires)
- Statutory Minimum Tread Depth: 1.6 mm (Recommends pull for retreading at 3.0 mm)
"""

from typing import List, Dict, Any


class TreadDepthLaserScanner:
    MIN_LEGAL_TREAD_MM = 1.6
    RETREAD_PULL_THRESHOLD_MM = 3.0

    @staticmethod
    def process_drive_over_scan(bus_number: str, tire_readings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates 6-wheel laser tread depth profile.
        """
        flagged_tires = []
        for t in tire_readings:
            pos = t.get('position', 'UNKNOWN')
            depth = t.get('tread_depth_mm', 14.0)

            if depth <= TreadDepthLaserScanner.MIN_LEGAL_TREAD_MM:
                flagged_tires.append({'position': pos, 'depth_mm': depth, 'action': 'IMMEDIATE_PULL_ILLEGAL_BALD'})
            elif depth <= TreadDepthLaserScanner.RETREAD_PULL_THRESHOLD_MM:
                flagged_tires.append({'position': pos, 'depth_mm': depth, 'action': 'SCHEDULE_PULL_FOR_RETREAD'})

        return {
            'bus_number': bus_number,
            'total_tires_scanned': len(tire_readings),
            'tires_requiring_action': len(flagged_tires),
            'flagged_tires': flagged_tires,
            'is_fleet_safe_for_service': len([f for f in flagged_tires if 'ILLEGAL' in f['action']]) == 0
        }
