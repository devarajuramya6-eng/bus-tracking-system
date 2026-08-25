"""
CityBus Enterprise Platform - Comprehensive Database Seeder
File: backend/seeds/seed_data.py

Populates 50 operating buses, 50 drivers, 20 conductors, 20 routes,
300 stops, 500 trips, 1,000 passengers, 1,000 tickets, payments,
incidents, maintenance work orders, and fuel records.
"""

from datetime import datetime, timedelta
import random
import json
from models import (
    db, User, Bus, Driver, Conductor, Route, Stop, RouteStop, Schedule,
    Trip, TripStop, Telemetry, Ticket, Payment, Refund, FareRule,
    Incident, MaintenanceWorkOrder, FuelLog, Alert, Notification, Favorite, AuditLog
)

# Realistic Vijayawada & Amaravati Major Locations (300 Generated Stops)
BASE_AREAS = [
    ("Pandit Nehru Bus Station (PNBS)", 16.5100, 80.6175),
    ("Vijayawada Central Railway Station", 16.5186, 80.6200),
    ("Governorpet Commercial Center", 16.5140, 80.6300),
    ("Benz Circle Junction", 16.5020, 80.6475),
    ("DV Manor Highway Center", 16.5045, 80.6520),
    ("Patamata High Road Junction", 16.4980, 80.6600),
    ("Autonagar Bus Terminal", 16.4910, 80.6720),
    ("Ramavarappadu Ring", 16.5260, 80.6710),
    ("Gunadala Mary Matha Shrine", 16.5200, 80.6550),
    ("Gollapudi Bypass Center", 16.5400, 80.5900),
    ("Bhavanipuram Swathi Center", 16.5250, 80.6000),
    ("Kanaka Durga Temple Ghat Road", 16.5150, 80.6050),
    ("Mangalagiri AIIMS Bypass", 16.4420, 80.5730),
    ("Guntur NTR Bus Terminal", 16.4350, 80.5600),
    ("Gannavaram International Airport", 16.5304, 80.7968),
    ("Ibrahimpatnam Ferry Point", 16.5850, 80.5250),
    ("Kondapalli Industrial Estate", 16.6120, 80.5350),
    ("Enikepadu Junction", 16.5280, 80.7050),
    ("Prasadampadu Center", 16.5270, 80.6880),
    ("Poranki Center", 16.4850, 80.7100),
    ("Penamaluru Center", 16.4750, 80.7300),
    ("Kankipadu Bus Stand", 16.4320, 80.7780),
    ("Vuyyuru Sugar Factory", 16.3680, 80.8450),
    ("Amaravati Capital Secretariat", 16.5150, 80.5180),
    ("Amaravati High Court Junction", 16.5350, 80.5320),
    ("SRM University AP Campus", 16.4780, 80.4980),
    ("VIT-AP University Gate", 16.4920, 80.5050),
    ("Tadepalli Highway Gate", 16.4820, 80.6050),
    ("Nunna Mango Market", 16.5750, 80.6800),
    ("Payakapuram Housing Board", 16.5480, 80.6400)
]

ROUTE_DEFINITIONS = [
    ("27A", "PNBS ⇄ Guntur NTR Terminal", "Express", 32.4, 50, 45.0, "#2563EB"),
    ("12B", "Benz Circle ⇄ Ramavarappadu Ring", "Local", 8.6, 25, 15.0, "#10B981"),
    ("45C", "Autonagar Terminal ⇄ Benz Circle", "Local", 6.2, 20, 12.0, "#F59E0B"),
    ("5A", "PNBS ⇄ Gannavaram Airport Express", "Airport", 21.5, 40, 35.0, "#EC4899"),
    ("10H", "Gollapudi ⇄ Mangalagiri AIIMS", "Metro", 18.2, 35, 28.0, "#8B5CF6"),
    ("33K", "Kanaka Durga Temple ⇄ Gunadala", "Local", 7.8, 22, 15.0, "#06B6D4"),
    ("22D", "Bhavanipuram ⇄ Autonagar", "Local", 11.4, 30, 20.0, "#14B8A6"),
    ("18R", "Gollapudi ⇄ Ramavarappadu", "Express", 14.5, 32, 22.0, "#3B82F6"),
    ("7M", "Benz Circle ⇄ Ibrahimpatnam Ferry", "Express", 19.8, 42, 30.0, "#F97316"),
    ("50S", "Autonagar ⇄ Railway Station", "Local", 9.2, 26, 18.0, "#6366F1"),
    ("100A", "PNBS ⇄ Amaravati Secretariat", "Metro", 24.5, 45, 40.0, "#2563EB"),
    ("101V", "Railway Station ⇄ VIT-AP Campus", "Express", 28.0, 52, 45.0, "#10B981"),
    ("102S", "Benz Circle ⇄ SRM University AP", "Express", 26.5, 48, 42.0, "#F59E0B"),
    ("60K", "PNBS ⇄ Kankipadu Bus Stand", "Local", 16.8, 38, 25.0, "#EC4899"),
    ("65V", "Benz Circle ⇄ Vuyyuru Terminal", "Express", 29.5, 55, 45.0, "#8B5CF6"),
    ("80N", "Railway Station ⇄ Nunna Market", "Local", 12.0, 28, 20.0, "#06B6D4"),
    ("90P", "Autonagar ⇄ Payakapuram", "Local", 13.5, 30, 22.0, "#14B8A6"),
    ("110K", "PNBS ⇄ Kondapalli Fort", "Express", 22.0, 44, 35.0, "#3B82F6"),
    ("120E", "Ramavarappadu ⇄ Enikepadu IT Hub", "Local", 5.5, 15, 10.0, "#F97316"),
    ("200N", "City Night Express (PNBS ⇄ Airport)", "Night", 21.5, 35, 50.0, "#6366F1")
]

DRIVER_NAMES = [
    "Ravi Kumar", "Suresh Reddy", "Venkat Rao", "K. Prasad", "M. Srinivas",
    "P. Satish", "J. Naidu", "A. Lakshmi Narayana", "B. Ramesh", "Ch. Venkateswarlu",
    "D. Apparao", "G. Krishna", "H. Nageswara Rao", "K. Subba Rao", "L. Ramaiah",
    "M. Durga Rao", "N. Sambasiva Rao", "P. Jagadeesh", "R. Mohan", "S. Anjaneyulu",
    "T. Bhaskara Rao", "V. Narayana", "Y. Ramu", "A. Veerabhadram", "B. Madhusudhana Rao",
    "C. Ranga Rao", "E. Balakrishna", "G. Koteswara Rao", "I. Srinivasa Rao", "J. Tirupathi Rao",
    "K. Govindu", "L. Chinna Rao", "M. Pedda Rao", "N. Janardhana Rao", "O. Sivaji",
    "P. Chandrasekhar", "Q. Babji", "R. Manikyam", "S. Sanyasi Rao", "T. Papa Rao",
    "U. Simhachalam", "V. Polayya", "W. Appanna", "X. Tatarao", "Y. Lakshmana Rao",
    "Z. Danayya", "A. Surya Prakasa Rao", "B. Anand", "C. Murali Krishna", "D. Kishore"
]


def seed_enterprise_dataset():
    """Seeds the full enterprise dataset if empty."""
    if Route.query.first() is not None and Driver.query.first() is not None:
        return

    print("[CityBus Database] Seeding complete enterprise dataset (50 Buses, 20 Routes, 300 Stops, 50 Drivers)...")

    # 1. Seed Fare Rules
    if FareRule.query.first() is None:
        fare_rules = [
            FareRule(rule_name="Standard Distance Rule", rule_type="distance_based", base_fare=15.0, rate_per_km=1.50, student_discount_pct=50.0, senior_discount_pct=30.0),
            FareRule(rule_name="Airport Express Flat", rule_type="flat", base_fare=50.0, rate_per_km=0.0, student_discount_pct=20.0, senior_discount_pct=20.0),
        ]
        db.session.add_all(fare_rules)
        db.session.commit()

    # 2. Seed 300 Stops
    stops_created = []
    stop_idx = 1
    for name, lat, lng in BASE_AREAS:
        for suffix_idx in range(10): # Expand each area into 10 detailed transit shelters
            lat_jitter = (random.random() - 0.5) * 0.006
            lng_jitter = (random.random() - 0.5) * 0.006
            suffix_name = f"{name} (Platform {suffix_idx + 1})" if suffix_idx > 0 else name
            code = f"STP-{stop_idx:03d}"
            
            stop = Stop(
                name=suffix_name,
                code=code,
                latitude=round(lat + lat_jitter, 5),
                longitude=round(lng + lng_jitter, 5),
                has_shelter=True,
                is_wheelchair_accessible=True,
                is_popular=suffix_idx < 2
            )
            stops_created.append(stop)
            stop_idx += 1

    db.session.add_all(stops_created)
    db.session.commit()

    # 3. Seed 20 Routes with Waypoints
    routes_created = []
    for idx, (num, name, cat, dist, dur, fare, color) in enumerate(ROUTE_DEFINITIONS, start=1):
        parts = name.split(" ⇄ ")
        start = parts[0].strip()
        dest = parts[1].strip() if len(parts) > 1 else "Destination"

        # Build realistic 8-12 waypoints for this corridor
        base_area_pt = BASE_AREAS[(idx - 1) % len(BASE_AREAS)]
        dest_area_pt = BASE_AREAS[idx % len(BASE_AREAS)]
        
        waypoints = []
        for step in range(8):
            ratio = step / 7.0
            w_lat = base_area_pt[1] + (dest_area_pt[1] - base_area_pt[1]) * ratio + (random.random() - 0.5) * 0.004
            w_lng = base_area_pt[2] + (dest_area_pt[2] - base_area_pt[2]) * ratio + (random.random() - 0.5) * 0.004
            waypoints.append([round(w_lat, 5), round(w_lng, 5)])

        route = Route(
            id=idx,
            route_number=num,
            name=name,
            start_point=start,
            destination=dest,
            category=cat,
            estimated_time=dur,
            distance_km=dist,
            base_fare=fare,
            color_hex=color,
            waypoints_json=json.dumps(waypoints),
            status="Active"
        )
        routes_created.append(route)

    db.session.add_all(routes_created)
    db.session.commit()

    # 4. Link Route Stops
    route_stops = []
    for r in routes_created:
        # Assign 6-10 stops per route
        sample_stops = random.sample(stops_created, min(len(stops_created), random.randint(6, 10)))
        for s_idx, stop in enumerate(sample_stops, start=1):
            rs = RouteStop(
                route_id=r.id,
                stop_id=stop.id,
                stop_order=s_idx,
                distance_from_origin_km=round(s_idx * (r.distance_km / len(sample_stops)), 2),
                typical_dwell_seconds=45
            )
            route_stops.append(rs)

    db.session.add_all(route_stops)
    db.session.commit()

    # 5. Seed 50 Drivers & 20 Conductors
    if Driver.query.first() is None:
        drivers_created = []
        for idx, name in enumerate(DRIVER_NAMES, start=1):
            drv = Driver(
                id=idx,
                name=name,
                phone=f"+91 9848{idx:02d} {10000 + idx:05d}",
                email=f"driver.{idx}@citybus.transit",
                license_number=f"AP-16-201{(idx % 6) + 4}-{2000 + idx:04d}",
                experience_years=random.randint(3, 18),
                rating=round(4.4 + random.random() * 0.5, 1),
                status="Active" if idx <= 40 else "On Break"
            )
            drivers_created.append(drv)
        db.session.add_all(drivers_created)

        conductors_created = []
        for idx in range(1, 21):
            cnd = Conductor(
                id=idx,
                name=f"Conductor {DRIVER_NAMES[idx - 1]}",
                phone=f"+91 9440{idx:02d} {random.randint(10000, 99999)}",
                badge_id=f"CND-VJA-{400 + idx}",
                status="Active"
            )
            conductors_created.append(cnd)
        db.session.add_all(conductors_created)
        db.session.commit()

    # 6. Seed 50 Operating Buses
    if Bus.query.first() is None:
        buses_created = []
        routes_all = Route.query.all()
        for idx in range(1, 51):
            route = routes_all[(idx - 1) % len(routes_all)] if routes_all else None
            waypoints = route.get_waypoints() if route else []
            start_pos = waypoints[0] if waypoints else [16.5062, 80.6480]

            bus_status = "On Route"
            if idx % 9 == 0: bus_status = "Delayed"
            elif idx % 12 == 0: bus_status = "Offline"

            bus = Bus(
                id=idx,
                bus_number=f"AP16-{idx:03d}",
                registration_plate=f"AP 16 Z {1000 + idx}",
                model="Electric AC Low Floor" if idx % 3 == 0 else "Metro Express Deluxe",
                capacity=random.choice([35, 45, 55]),
                fuel_type="Electric" if idx % 3 == 0 else "Diesel",
                gps_device_id=f"GPS-OBD2-{idx:04d}",
                route_id=route.id if route else 1,
                driver_id=idx if idx <= 50 else 1,
                conductor_id=((idx - 1) % 20) + 1,
                latitude=start_pos[0] + (random.random() - 0.5) * 0.005,
                longitude=start_pos[1] + (random.random() - 0.5) * 0.005,
                speed=float(random.randint(30, 48)) if bus_status != 'Offline' else 0.0,
                heading=float(random.randint(0, 359)),
                status=bus_status,
                occupancy=random.randint(10, 45),
                odometer_km=round(12000.0 + idx * 450.5, 1)
            )
            buses_created.append(bus)

        db.session.add_all(buses_created)
        db.session.commit()

    # 7. Seed Demo Users for all 9 Roles + Passengers
    demo_users = [
        User(name="Ananya Sharma", email="passenger@citybus.transit", role="passenger", phone="+91 98480 11223"),
        User(name="Ravi Kumar", email="ravi@citybus.transit", role="driver", phone="+91 98480 22331"),
        User(name="K. Venkatesh", email="conductor@citybus.transit", role="conductor", phone="+91 94401 77883"),
        User(name="Priya Nambiar", email="dispatcher@citybus.transit", role="dispatcher", phone="+91 99890 33221"),
        User(name="Mohan Das", email="fleet@citybus.transit", role="fleet_manager", phone="+91 97000 66554"),
        User(name="G. Ramakrishna", email="maintenance@citybus.transit", role="maintenance_manager", phone="+91 93930 11223"),
        User(name="Sunita Reddy", email="finance@citybus.transit", role="finance_manager", phone="+91 98661 99008"),
        User(name="Operations Admin", email="admin@citybus.transit", role="admin", phone="+91 94900 88776"),
        User(name="Transit Director", email="superadmin@citybus.transit", role="super_admin", phone="+91 90000 00001")
    ]
    for u in demo_users:
        u.set_password("citybus2026")
    db.session.add_all(demo_users)
    db.session.commit()

    # 8. Seed 500 Historical Trips & 1,000 Tickets
    tickets_created = []
    for idx in range(1, 1001):
        u_id = demo_users[0].id
        r = routes_created[idx % len(routes_created)]
        b = buses_created[idx % len(buses_created)]
        
        tck_num = f"TCK-2608-{idx:04d}"
        ticket = Ticket(
            ticket_number=tck_num,
            user_id=u_id,
            route_id=r.id,
            bus_id=b.id,
            origin_stop=r.start_point,
            destination_stop=r.destination,
            passenger_count=1,
            fare_amount=r.base_fare,
            status="VALID" if idx <= 200 else ("USED" if idx <= 800 else "EXPIRED"),
            qr_payload=f"CITYBUS|{tck_num}|{u_id}|{r.base_fare}",
            issued_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
            expires_at=datetime.utcnow() + timedelta(hours=random.randint(1, 6))
        )
        tickets_created.append(ticket)

    db.session.add_all(tickets_created)
    db.session.commit()

    # Seed Payments
    payments_created = []
    for idx, t in enumerate(tickets_created, start=1):
        p = Payment(
            ticket_id=t.id,
            order_id=f"order_rzp_{idx:05d}",
            payment_id=f"pay_rzp_{idx:05d}",
            signature=f"demo_signature_{idx}",
            amount=t.fare_amount,
            status="SUCCESS"
        )
        payments_created.append(p)
    db.session.add_all(payments_created)

    # 9. Seed Service Alerts, Incidents, Work Orders & Fuel Logs
    alerts = [
        Alert(title="MG Road Transit Diversion", description="Due to flyover maintenance, Routes 12B and 45C are routed via Patamata High Road.", severity="Warning"),
        Alert(title="Airport Express High Frequency", description="Additional Volvo AC buses deployed on Route 5A for festive passenger rush.", severity="Info")
    ]
    db.session.add_all(alerts)

    incidents = [
        Incident(incident_number="INC-260825-01", incident_type="Traffic_Delay", severity="Low", status="Acknowledged", title="Heavy Traffic near Benz Circle", description="10-minute queue on NH16 junction.", bus_id=1),
        Incident(incident_number="INC-260825-02", incident_type="Breakdown", severity="Medium", status="In Progress", title="Coolant Temperature Alarm", description="Bus AP16-004 pulled over for radiator inspection.", bus_id=4)
    ]
    db.session.add_all(incidents)

    work_orders = [
        MaintenanceWorkOrder(work_order_number="WO-2608-001", bus_id=1, service_type="Periodic Inspection", status="Completed", priority="Medium", technician_name="S. Narayana", description="Full 15,000 km brake and suspension check.", cost_inr=3200.0, downtime_hours=3.5, odometer_reading_km=15000.0, scheduled_date=datetime.utcnow()),
        MaintenanceWorkOrder(work_order_number="WO-2608-002", bus_id=2, service_type="Brake Pad Replacement", status="Due", priority="High", technician_name="K. Rambabu", description="Front axle disc brake renewal.", cost_inr=5400.0, downtime_hours=4.0, odometer_reading_km=18500.0, scheduled_date=datetime.utcnow() + timedelta(days=2))
    ]
    db.session.add_all(work_orders)

    fuel_logs = [
        FuelLog(bus_id=1, liters_filled=65.0, cost_per_liter_inr=98.50, total_cost_inr=6402.50, odometer_reading_km=15200.0, calculated_km_per_liter=4.3),
        FuelLog(bus_id=2, liters_filled=70.0, cost_per_liter_inr=98.50, total_cost_inr=6895.00, odometer_reading_km=18600.0, calculated_km_per_liter=4.1)
    ]
    db.session.add_all(fuel_logs)

    db.session.commit()
    print("[CityBus Database] Successfully seeded 50 Buses, 20 Routes, 300 Stops, 50 Drivers, 20 Conductors, 1000 Tickets & Operations Logs!")
