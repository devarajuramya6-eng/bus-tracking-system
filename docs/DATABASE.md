# CityBus Enterprise Platform - Database Schema & ERD

## 1. Relational Database Schema Overview
The platform utilizes a 3NF normalized relational schema compatible with PostgreSQL (with PostGIS spatial extensions) and SQLite.

### Key Normalized Tables:
1. `users`: Stores user identity, bcrypt/SHA256 password hash, RBAC role (`passenger`, `driver`, `conductor`, `dispatcher`, `admin`, etc.), active status.
2. `buses`: Fleet inventory with vehicle code, registration plate, model, capacity, fuel type, GPS device ID, real-time latitude/longitude, heading, speed, status, occupancy, and odometer.
3. `drivers`: Licensed fleet operators, license expiration dates, experience years, and ratings.
4. `conductors`: Fare collection crew profiles, employee badge IDs.
5. `routes`: Transit corridors with start point, destination, category (`Express`, `Local`, `Metro`, `Airport`, `Night`), distance (km), estimated time (min), base fare, color code, and waypoints polyline JSON.
6. `stops`: Physical transit stops with geo-coordinates, shelter flag, wheelchair accessibility, and popularity index.
7. `route_stops`: Junction sequence table linking Stops to Routes in exact order with distance offsets and typical dwell seconds.
8. `schedules`: Master timetable definitions by service type (`Weekday`, `Weekend`, `Holiday`).
9. `trips`: Driver trip operational instances with start/stop timestamps, boarded passenger counts, and fare totals.
10. `trip_stops`: Granular stop-by-stop arrival and departure execution logs for on-time performance (OTP) computation.
11. `telemetries`: High-frequency historical GPS telemetry coordinate log.
12. `tickets`: Digital passes with unique ticket numbers, status state machine (`VALID`, `USED`, `EXPIRED`, `CANCELLED`, `REFUNDED`), and HMAC-SHA256 cryptographically signed QR payloads.
13. `payments`: Financial ledger recording Razorpay order IDs, payment IDs, signatures, and settlement status.
14. `refunds`: Cancellation and refund processing logs.
15. `fare_rules`: Distance and flat fare calculation matrix with concession discount rules.
16. `incidents`: Operational breakdowns, traffic congestion, medical alerts, and Emergency SOS panic triggers.
17. `maintenance_work_orders`: Preventive maintenance logs, replacement parts, cost (INR), downtime hours, and technician assignments.
18. `fuel_logs`: Refill transactions, liters filled, pump stations, and calculated fuel efficiency (km/L).
19. `alerts`: Public transit disruption broadcasts.
20. `notifications`: In-app passenger notifications.
21. `favorites`: Passenger bookmarked buses, routes, and stops.
22. `audit_logs`: Security and administrative compliance log.
