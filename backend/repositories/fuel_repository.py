"""
CityBus Enterprise Platform - Fuel & Energy Repository
File: backend/repositories/fuel_repository.py

Encapsulates vehicle refueling records, EV battery charging logs,
energy efficiency metrics (km/L, kWh/km), and fuel cost accounting.
"""

from datetime import datetime
from models import db, FuelLog, Bus
from sqlalchemy import or_, desc, func


class FuelRepository:
    """Data access layer for depot fuel logs and energy consumption."""

    @staticmethod
    def get_all(bus_id=None, page=1, per_page=20):
        """Retrieves fuel logs with optional bus filtering and pagination."""
        query = FuelLog.query
        if bus_id:
            query = query.filter_by(bus_id=bus_id)
            
        total = query.count()
        logs = query.order_by(FuelLog.date.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return logs, total

    @staticmethod
    def get_by_id(log_id):
        """Fetches single fuel log by ID."""
        return FuelLog.query.get(log_id)

    @staticmethod
    def create(bus_id, quantity, cost, odometer_km=None, station_location="Central Depot Pump 1", fuel_type="Diesel"):
        """Records a new fueling or EV fast-charging session."""
        bus = Bus.query.get(bus_id)
        if not bus:
            return None, "Bus not found"
            
        current_odometer = odometer_km or bus.odometer_km
        
        # Calculate efficiency from last log if available
        last_log = FuelLog.query.filter_by(bus_id=bus_id).order_by(FuelLog.date.desc()).first()
        efficiency = None
        if last_log and current_odometer and last_log.odometer_km:
            km_diff = current_odometer - last_log.odometer_km
            if km_diff > 0 and quantity > 0:
                efficiency = round(km_diff / quantity, 2)
                
        log = FuelLog(
            bus_id=bus_id,
            quantity=float(quantity),
            cost=float(cost),
            odometer_km=float(current_odometer),
            efficiency=efficiency,
            fuel_type=fuel_type,
            station_location=station_location,
            date=datetime.utcnow()
        )
        db.session.add(log)
        
        # Update bus odometer
        if current_odometer > bus.odometer_km:
            bus.odometer_km = current_odometer
            
        db.session.commit()
        return log, None

    @staticmethod
    def get_fleet_fuel_summary():
        """Calculates total energy expenditure and average efficiency across the fleet."""
        total_logs = FuelLog.query.count()
        total_liters = db.session.query(func.sum(FuelLog.quantity)).scalar() or 0.0
        total_cost = db.session.query(func.sum(FuelLog.cost)).scalar() or 0.0
        avg_efficiency = db.session.query(func.avg(FuelLog.efficiency)).filter(FuelLog.efficiency.isnot(None)).scalar() or 0.0
        
        return {
            "total_refuel_events": total_logs,
            "total_fuel_quantity": round(float(total_liters), 2),
            "total_expenditure_inr": round(float(total_cost), 2),
            "average_efficiency_kml": round(float(avg_efficiency), 2)
        }
