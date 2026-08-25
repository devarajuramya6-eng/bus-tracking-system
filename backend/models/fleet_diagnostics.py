import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Float, Boolean, Text
from sqlalchemy.orm import relationship

try:
    from backend.database import Base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

class FleetDiagnostics(Base):
    """
    Detailed Fleet Diagnostics model for real-time and historical vehicle telemetry.
    Tracks extensive data points from IoT sensors installed on the buses.
    """
    __tablename__ = "fleet_diagnostics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    bus_id = Column(String(36), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Core Telemetry
    speed_kmh = Column(Float, nullable=False, default=0.0)
    engine_rpm = Column(Integer, nullable=True)
    fuel_level_percent = Column(Float, nullable=True)
    battery_voltage = Column(Float, nullable=True)
    engine_temperature_celsius = Column(Float, nullable=True)
    
    # Advanced Diagnostics
    oil_pressure_kpa = Column(Float, nullable=True)
    transmission_temperature_celsius = Column(Float, nullable=True)
    brake_pad_wear_percent = Column(Float, nullable=True)
    tire_pressure_psi = Column(JSON, nullable=True) # E.g., {"FL": 110, "FR": 109, "RL": 112, "RR": 111}
    
    # Environmental & Passenger Comfort
    internal_temperature_celsius = Column(Float, nullable=True)
    hvac_status = Column(String(20), nullable=True) # "ON_COOL", "ON_HEAT", "OFF", "DEFROST"
    ambient_light_level = Column(Float, nullable=True)
    air_quality_index = Column(Integer, nullable=True)
    
    # Location and Heading
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    heading_degrees = Column(Float, nullable=True)
    gps_accuracy_meters = Column(Float, nullable=True)
    
    # Operational Status
    doors_open = Column(Boolean, default=False)
    wiper_status = Column(String(20), default="OFF")
    headlights_on = Column(Boolean, default=False)
    
    # Errors and Alerts
    active_dtc_codes = Column(JSON, nullable=True) # Diagnostic Trouble Codes
    critical_alert = Column(Boolean, default=False, index=True)
    alert_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<FleetDiagnostics Bus:{self.bus_id} at {self.timestamp}>"

    def to_dict(self):
        return {
            "id": self.id,
            "bus_id": self.bus_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "speed_kmh": self.speed_kmh,
            "engine_rpm": self.engine_rpm,
            "fuel_level_percent": self.fuel_level_percent,
            "battery_voltage": self.battery_voltage,
            "engine_temperature_celsius": self.engine_temperature_celsius,
            "oil_pressure_kpa": self.oil_pressure_kpa,
            "transmission_temperature_celsius": self.transmission_temperature_celsius,
            "brake_pad_wear_percent": self.brake_pad_wear_percent,
            "tire_pressure_psi": self.tire_pressure_psi,
            "internal_temperature_celsius": self.internal_temperature_celsius,
            "hvac_status": self.hvac_status,
            "air_quality_index": self.air_quality_index,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "heading_degrees": self.heading_degrees,
            "doors_open": self.doors_open,
            "active_dtc_codes": self.active_dtc_codes,
            "critical_alert": self.critical_alert
        }
