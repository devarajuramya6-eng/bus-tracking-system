"""
CityBus Enterprise Platform - Digital Out-Of-Home (DOOH) Transit Advertising Service
File: backend/services/transit_advertising_service.py

Manages on-board LCD screen advertisements, side-wrap exterior brand campaigns,
geofenced location-triggered audio spots, and ad revenue analytics.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from repositories.audit_repository import AuditRepository


class TransitAdCampaign:
    def __init__(self, campaign_id: str, client_name: str, ad_title: str, format_type: str,
                 daily_budget_inr: float, target_corridor: Optional[str] = None):
        self.campaign_id = campaign_id
        self.client_name = client_name
        self.ad_title = ad_title
        self.format_type = format_type  # LCD_IN_CABIN_VIDEO, BUS_SIDE_WRAP, BUS_STOP_POSTER, GEOFENCED_AUDIO
        self.daily_budget_inr = daily_budget_inr
        self.target_corridor = target_corridor
        self.impressions_served = 0
        self.status = "ACTIVE"


class TransitAdvertisingService:
    """Manages DOOH digital advertising on transit vehicle displays and bus stops."""

    _campaigns: Dict[str, TransitAdCampaign] = {
        "AD-ANDHRA-BANK": TransitAdCampaign("AD-ANDHRA-BANK", "Union Bank of India", "Digital Home Loan 6.8% Campaign", "LCD_IN_CABIN_VIDEO", 1500.0, "27A"),
        "AD-KLU-UNIV":   TransitAdCampaign("AD-KLU-UNIV", "KL University Vaddeswaram", "B.Tech Admissions 2026", "BUS_SIDE_WRAP", 2800.0, "All Corridors"),
        "AD-AP-TOURISM": TransitAdCampaign("AD-AP-TOURISM", "AP Tourism Development Corp", "Explore Bhavani Island Wonders", "LCD_IN_CABIN_VIDEO", 1200.0, "5A")
    }

    @classmethod
    def get_active_campaigns(cls) -> List[Dict[str, Any]]:
        """Returns currently playing ad campaigns."""
        return [
            {
                "campaign_id": c.campaign_id,
                "client_name": c.client_name,
                "ad_title": c.ad_title,
                "format_type": c.format_type,
                "daily_budget_inr": c.daily_budget_inr,
                "target_corridor": c.target_corridor,
                "impressions_served": c.impressions_served,
                "status": c.status
            }
            for c in cls._campaigns.values()
        ]

    @classmethod
    def log_impression(cls, campaign_id: str, bus_id: int) -> bool:
        """Logs display impression playback on vehicle LCD."""
        c = cls._campaigns.get(campaign_id)
        if not c:
            return False
        c.impressions_served += 1
        return True
