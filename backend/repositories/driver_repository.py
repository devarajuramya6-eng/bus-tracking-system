"""
CityBus Enterprise Platform - Driver Repository
File: backend/repositories/driver_repository.py

Encapsulates data access and operations for Driver records, shifts,
performance statistics, and fleet vehicle assignments.
"""

from datetime import datetime
from models import db, Driver, Bus, Trip, User
from sqlalchemy import or_, desc


class DriverRepository:
    """Data access layer for transit vehicle operators."""

    @staticmethod
    def get_all(status=None, search=None, page=1, per_page=20):
        """Retrieves drivers with optional status and search filtering with pagination."""
        query = Driver.query
        if status and status != 'all':
            query = query.filter_by(status=status)
        if search:
            s = f"%{search}%"
            query = query.filter(or_(
                Driver.name.ilike(s),
                Driver.phone.ilike(s),
                Driver.email.ilike(s),
                Driver.license_number.ilike(s)
            ))
        
        total = query.count()
        drivers = query.order_by(Driver.id.asc()).offset((page - 1) * per_page).limit(per_page).all()
        return drivers, total

    @staticmethod
    def get_by_id(driver_id):
        """Fetches a single driver by primary key ID."""
        return Driver.query.get(driver_id)

    @staticmethod
    def get_by_email(email):
        """Fetches a single driver by email address."""
        return Driver.query.filter_by(email=email.strip().lower()).first()

    @staticmethod
    def create(name, phone, email=None, license_number=None, experience_years=3, rating=4.8, status='Active'):
        """Creates and persists a new driver record."""
        driver = Driver(
            name=name.strip(),
            phone=phone.strip(),
            email=email.strip().lower() if email else None,
            license_number=license_number.strip() if license_number else None,
            experience_years=experience_years,
            rating=rating,
            status=status
        )
        db.session.add(driver)
        db.session.commit()
        return driver

    @staticmethod
    def update(driver_id, **kwargs):
        """Updates driver attributes."""
        driver = Driver.query.get(driver_id)
        if not driver:
            return None
        
        for key, val in kwargs.items():
            if hasattr(driver, key) and key != 'id':
                setattr(driver, key, val)
        
        db.session.commit()
        return driver

    @staticmethod
    def delete(driver_id):
        """Deletes a driver record if no active trips exist."""
        driver = Driver.query.get(driver_id)
        if not driver:
            return False, "Driver not found"
        
        active_trips = Trip.query.filter_by(driver_id=driver_id, status='Active').count()
        if active_trips > 0:
            return False, "Cannot delete driver with active trips in progress"
        
        # Unassign any assigned buses
        assigned_buses = Bus.query.filter_by(driver_id=driver_id).all()
        for bus in assigned_buses:
            bus.driver_id = None
            
        db.session.delete(driver)
        db.session.commit()
        return True, None

    @staticmethod
    def get_active_trip(driver_id):
        """Returns the currently active trip for a driver."""
        return Trip.query.filter_by(driver_id=driver_id, status='Active').order_by(Trip.id.desc()).first()

    @staticmethod
    def get_trip_history(driver_id, limit=20):
        """Retrieves recent completed trips for a driver."""
        return Trip.query.filter_by(driver_id=driver_id).order_by(Trip.start_time.desc()).limit(limit).all()

    @staticmethod
    def get_driver_statistics(driver_id):
        """Calculates operational metrics for driver performance."""
        driver = Driver.query.get(driver_id)
        if not driver:
            return None
            
        trips = Trip.query.filter_by(driver_id=driver_id).all()
        completed_trips = [t for t in trips if t.status == 'Completed']
        
        total_duration_minutes = 0
        for t in completed_trips:
            if t.end_time and t.start_time:
                total_duration_minutes += (t.end_time - t.start_time).total_seconds() / 60.0
                
        avg_trip_time = round(total_duration_minutes / max(1, len(completed_trips)), 1)
        
        return {
            "driver_id": driver.id,
            "name": driver.name,
            "status": driver.status,
            "rating": driver.rating,
            "experience_years": driver.experience_years,
            "total_trips": len(trips),
            "completed_trips": len(completed_trips),
            "active_trip_id": driver.get_active_trip_id(),
            "average_trip_minutes": avg_trip_time,
            "assigned_bus": driver.buses[0].to_dict() if driver.buses else None
        }
