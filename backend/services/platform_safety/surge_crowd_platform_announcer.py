"""
CityBus Enterprise Platform - Surge Crowd Platform Bypass Audio Announcer
File: backend/services/platform_safety/surge_crowd_platform_announcer.py

Generates automatic platform announcements during peak crush congestion:
- Detects crush-loaded buses (> 90% full) and alerts waiting commuters on platforms
- Directs commuters to empty trailing follower buses arriving within 2-4 minutes
"""

from typing import Dict, Any


class SurgeCrowdAnnouncer:
    @staticmethod
    def evaluate_platform_announcement(approaching_bus_number: str,
                                       approaching_bus_occ_pct: float,
                                       trailing_bus_number: str,
                                       trailing_bus_eta_min: float,
                                       trailing_bus_occ_pct: float) -> Dict[str, Any]:
        """
        Creates platform guidance announcement.
        """
        if approaching_bus_occ_pct >= 90.0:
            announcement_en = f"Notice: Approaching bus {approaching_bus_number} is currently full. Next bus {trailing_bus_number} has available seats and will arrive in {int(trailing_bus_eta_min)} minutes."
            announcement_te = f"గమనిక: వస్తున్న బస్సు {approaching_bus_number} పూర్తిగా నిండిపోయింది. తదుపరి బస్సు {trailing_bus_number} {int(trailing_bus_eta_min)} నిమిషాల్లో ఖాళీ సీట్లతో చేరుకుంటుంది."
            bypass_recommended = True
        else:
            announcement_en = f"Approaching bus {approaching_bus_number} has seats available. Please board through the front doors."
            announcement_te = f"వస్తున్న బస్సు {approaching_bus_number} లో సీట్లు అందుబాటులో ఉన్నాయి. దయచేసి ముందు ద్వారం నుండి ఎక్కండి."
            bypass_recommended = False

        return {
            'approaching_bus': approaching_bus_number,
            'approaching_occupancy_pct': round(approaching_bus_occ_pct, 1),
            'trailing_bus': trailing_bus_number,
            'trailing_bus_eta_min': round(trailing_bus_eta_min, 1),
            'is_crowd_bypass_active': bypass_recommended,
            'announcement_english': announcement_en,
            'announcement_telugu': announcement_te
        }
