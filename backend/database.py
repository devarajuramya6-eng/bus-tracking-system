"""
CityBus - Database Setup & Demo Data Seeder (database.py)

Initializes SQLAlchemy database connection and automatically populates
realistic sample data for Vijayawada (10 buses, 5 routes, 15 stops, 8 drivers, 3 demo users)
when the database is created for the first time.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    """Binds SQLAlchemy to the Flask app, creates all tables, and seeds initial data."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_demo_data()


def seed_demo_data():
    """Seeds sample routes, drivers, stops, buses, and users if database is empty."""
    from models import Route, Driver, Stop, Bus, User

    # Only seed if routes table is empty
    if Route.query.first() is not None:
        return

    print("[CityBus Database] Initializing SQLite database and seeding demo data...")

    # 1. Seed 5 Transit Routes
    routes_data = [
        Route(id=1, route_number="27A", start_point="Vijayawada", destination="Guntur", estimated_time=55, status="Active"),
        Route(id=2, route_number="12B", start_point="Benz Circle", destination="Ramavarappadu", estimated_time=25, status="Active"),
        Route(id=3, route_number="45C", start_point="Autonagar", destination="Benz Circle", estimated_time=20, status="Active"),
        Route(id=4, route_number="18A", start_point="PNBS", destination="Gannavaram Airport", estimated_time=40, status="Active"),
        Route(id=5, route_number="22B", start_point="Gollapudi", destination="Mangalagiri AIIMS", estimated_time=35, status="Active"),
    ]
    db.session.add_all(routes_data)
    db.session.commit()

    # 2. Seed 8 Fleet Drivers
    drivers_data = [
        Driver(id=1, name="Ravi Kumar", phone="+91 98480 22331", email="ravi.kumar@citybus.transit", status="Active"),
        Driver(id=2, name="Suresh Reddy", phone="+91 98481 44552", email="suresh.reddy@citybus.transit", status="Active"),
        Driver(id=3, name="Venkat Rao", phone="+91 94401 77883", email="venkat.rao@citybus.transit", status="Active"),
        Driver(id=4, name="K. Prasad", phone="+91 99890 33221", email="prasad.k@citybus.transit", status="Active"),
        Driver(id=5, name="M. Srinivas", phone="+91 97000 66554", email="srinivas.m@citybus.transit", status="Active"),
        Driver(id=6, name="P. Satish", phone="+91 93930 11223", email="satish.p@citybus.transit", status="Break"),
        Driver(id=7, name="J. Naidu", phone="+91 98661 99008", email="naidu.j@citybus.transit", status="Active"),
        Driver(id=8, name="A. Lakshmi Narayana", phone="+91 94900 88776", email="lakshmi.a@citybus.transit", status="Active"),
    ]
    db.session.add_all(drivers_data)
    db.session.commit()

    # 3. Seed 15 Bus Stops across Vijayawada
    stops_data = [
        # Route 1: 27A (Vijayawada -> Guntur)
        Stop(route_id=1, name="Pandit Nehru Bus Station (PNBS)", latitude=16.5100, longitude=80.6175, stop_order=1),
        Stop(route_id=1, name="Governorpet Central", latitude=16.5140, longitude=80.6300, stop_order=2),
        Stop(route_id=1, name="Benz Circle Junction", latitude=16.5020, longitude=80.6475, stop_order=3),
        Stop(route_id=1, name="DV Manor Center", latitude=16.5045, longitude=80.6520, stop_order=4),
        Stop(route_id=1, name="Patamata High Road", latitude=16.4980, longitude=80.6600, stop_order=5),
        Stop(route_id=1, name="Mangalagiri AIIMS Bypass", latitude=16.4420, longitude=80.5730, stop_order=6),
        Stop(route_id=1, name="Guntur NTR Bus Terminal", latitude=16.4350, longitude=80.5600, stop_order=7),

        # Route 2: 12B (Benz Circle -> Ramavarappadu)
        Stop(route_id=2, name="Benz Circle Junction", latitude=16.5020, longitude=80.6475, stop_order=1),
        Stop(route_id=2, name="DV Manor Center", latitude=16.5045, longitude=80.6520, stop_order=2),
        Stop(route_id=2, name="Gunadala Mary Matha Shrine", latitude=16.5200, longitude=80.6550, stop_order=3),
        Stop(route_id=2, name="Ramavarappadu Ring", latitude=16.5260, longitude=80.6710, stop_order=4),

        # Route 3: 45C (Autonagar -> Benz Circle)
        Stop(route_id=3, name="Autonagar Bus Terminal", latitude=16.4910, longitude=80.6720, stop_order=1),
        Stop(route_id=3, name="Patamata High Road", latitude=16.4980, longitude=80.6600, stop_order=2),
        Stop(route_id=3, name="Benz Circle Junction", latitude=16.5020, longitude=80.6475, stop_order=3),

        # Route 4: 18A (PNBS -> Gannavaram Airport)
        Stop(route_id=4, name="Pandit Nehru Bus Station (PNBS)", latitude=16.5100, longitude=80.6175, stop_order=1),
        Stop(route_id=4, name="Vijayawada Railway Station", latitude=16.5186, longitude=80.6200, stop_order=2),
        Stop(route_id=4, name="Gunadala Mary Matha Shrine", latitude=16.5200, longitude=80.6550, stop_order=3),
        Stop(route_id=4, name="Ramavarappadu Ring", latitude=16.5260, longitude=80.6710, stop_order=4),
        Stop(route_id=4, name="Gannavaram International Airport", latitude=16.5304, longitude=80.7968, stop_order=5),

        # Route 5: 22B (Gollapudi -> Mangalagiri AIIMS)
        Stop(route_id=5, name="Gollapudi Center", latitude=16.5400, longitude=80.5900, stop_order=1),
        Stop(route_id=5, name="Bhavanipuram Swathi Center", latitude=16.5250, longitude=80.6000, stop_order=2),
        Stop(route_id=5, name="Kanaka Durga Temple Ghat Road", latitude=16.5150, longitude=80.6050, stop_order=3),
        Stop(route_id=5, name="Pandit Nehru Bus Station (PNBS)", latitude=16.5100, longitude=80.6175, stop_order=4),
        Stop(route_id=5, name="Mangalagiri AIIMS Bypass", latitude=16.4420, longitude=80.5730, stop_order=5),
    ]
    db.session.add_all(stops_data)
    db.session.commit()

    # 4. Seed 10 Operating Buses with Realistic Vijayawada GPS Positions
    buses_data = [
        Bus(id=1, bus_number="27A", route_id=1, driver_id=1, latitude=16.5062, longitude=80.6480, speed=38.0, status="On Route", last_updated=datetime.utcnow()),
        Bus(id=2, bus_number="12B", route_id=2, driver_id=2, latitude=16.5075, longitude=80.6495, speed=32.0, status="On Route", last_updated=datetime.utcnow()),
        Bus(id=3, bus_number="45C", route_id=3, driver_id=3, latitude=16.5150, longitude=80.6400, speed=25.0, status="Delayed", last_updated=datetime.utcnow()),
        Bus(id=4, bus_number="18A", route_id=4, driver_id=4, latitude=16.5260, longitude=80.6710, speed=48.0, status="On Route", last_updated=datetime.utcnow()),
        Bus(id=5, bus_number="22B", route_id=5, driver_id=5, latitude=16.5180, longitude=80.6250, speed=30.0, status="On Route", last_updated=datetime.utcnow()),
        Bus(id=6, bus_number="30C", route_id=2, driver_id=6, latitude=16.5150, longitude=80.6050, speed=0.0, status="Offline", last_updated=datetime.utcnow()),
        Bus(id=7, bus_number="41A", route_id=5, driver_id=7, latitude=16.4800, longitude=80.6000, speed=42.0, status="On Route", last_updated=datetime.utcnow()),
        Bus(id=8, bus_number="55B", route_id=4, driver_id=8, latitude=16.5210, longitude=80.6400, speed=35.0, status="On Route", last_updated=datetime.utcnow()),
        Bus(id=9, bus_number="61C", route_id=3, driver_id=3, latitude=16.5045, longitude=80.6520, speed=18.0, status="Delayed", last_updated=datetime.utcnow()),
        Bus(id=10, bus_number="72A", route_id=1, driver_id=2, latitude=16.4980, longitude=80.6600, speed=36.0, status="On Route", last_updated=datetime.utcnow()),
    ]
    db.session.add_all(buses_data)
    db.session.commit()

    # 5. Seed 3 Demo Users for Authentication
    users_data = [
        User(name="Passenger User", email="passenger@citybus.transit", password="citybus2026", role="passenger"),
        User(name="Ravi Kumar", email="ravi@citybus.transit", password="citybus2026", role="driver"),
        User(name="Operations Admin", email="admin@citybus.transit", password="citybus2026", role="admin"),
    ]
    db.session.add_all(users_data)
    db.session.commit()

    print("[CityBus Database] Successfully seeded 10 buses, 5 routes, 15 stops, 8 drivers, and 3 users.")
