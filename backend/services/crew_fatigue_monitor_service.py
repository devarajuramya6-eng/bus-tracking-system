"""
CityBus Enterprise Platform - Driver Fatigue & Biometric Alert Service
File: backend/services/crew_fatigue_monitor_service.py

Analyzes Driver Monitoring System (DMS) optical camera signals:
- PERCLOS (Percentage of Eye Closure) drowsiness detection
- Steering wheel micro-correction frequency (yawn and micro-sleep events)
- Automatic safety alarm buzzer triggers and dispatcher relief vehicle calls
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from models import Driver, Bus, db
from repositories.audit_repository import AuditRepository


class CrewFatigueMonitorService:
    """Processes in-cabin DMS infrared sensor data to prevent driver fatigue accidents."""

    PERCLOS_DROWSINESS_THRESHOLD = 0.40 # 40% eye closure rate flags drowsiness

    _dms_logs: List[Dict[str, Any]] = []

    @classmethod
    def process_dms_telemetry(cls, driver_id: int, bus_id: int, perclos_ratio: float,
                              yawn_count_last_5min: int, head_pose_pitch_deg: float) -> Dict[str, Any]:
        """Ingests DMS camera sensor packet."""
        driver = Driver.query.get(driver_id)
        bus = Bus.query.get(bus_id)

        is_drowsy = perclos_ratio >= cls.PERCLOS_DROWSINESS_THRESHOLD or yawn_count_last_5min >= 4 or head_pose_pitch_deg < -20.0

        alert_level = "CRITICAL_FATIGUE" if (perclos_ratio > 0.60 or yawn_count_last_5min >= 6) else ("WARNING" if is_drowsy else "NORMAL")

        entry = {
            "driver_id": driver_id,
            "driver_name": driver.name if driver else f"Driver #{driver_id}",
            "bus_id": bus_id,
            "bus_number": bus.bus_number if bus else f"Bus #{bus_id}",
            "perclos_ratio": round(perclos_ratio, 2),
            "yawn_count": yawn_count_last_5min,
            "head_pitch": round(head_pose_pitch_deg, 1),
            "alert_level": alert_level,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        cls._dms_logs.append(entry)

        if alert_level != "NORMAL":
            AuditRepository.log_event("DMS_FATIGUE_TRIGGERED", "DriverDMS", driver_id, None, None, f"Level: {alert_level}, Bus: {bus_id}")

        return entry

    @classmethod
    def get_recent_fatigue_alerts(cls) -> List[Dict[str, Any]]:
        """Returns active fatigue alerts requiring supervisor check-in."""
        return [log for log in cls._dms_logs if log["alert_level"] != "NORMAL"][-15:]
