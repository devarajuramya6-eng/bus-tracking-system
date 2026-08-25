# CityBus Enterprise Transit Architecture Document

## 1. System Overview
CityBus is a production-grade, full-stack intelligent public transportation management platform engineered for municipal transit authorities, operators, drivers, conductors, tactical dispatchers, and millions of daily commuters.

```
+---------------------------------------------------------------------------------------------------+
|                                 CLIENT APPLICATIONS & PORTALS                                     |
|  +-------------------+  +-------------------+  +-------------------+  +-------------------------+ |
|  |  Passenger PWA    |  |  Driver Cockpit   |  |  Conductor POS    |  |  Dispatcher Radar &     | |
|  |  (Live Map, ETA,  |  |  (GPS Telemetry,  |  |  (Camera QR       |  |  Admin Portal (Kanban,  | |
|  |   Pass Wallet)    |  |   SOS Panic HUD)  |  |   Scanner & POS)  |  |   Visual Route Editor)  | |
|  +---------+---------+  +---------+---------+  +---------+---------+  +------------+------------+ |
+------------|----------------------|----------------------|-------------------------|--------------+
             |                      |                      |                         |
             +----------------------+-----------+----------+-------------------------+
                                                | HTTP / HTTPS / WebSocket (WSS)
                                                v
+---------------------------------------------------------------------------------------------------+
|                                 ENTERPRISE APPLICATION GATEWAY                                    |
|                                         (Nginx Reverse Proxy)                                     |
+-----------------------------------------------+---------------------------------------------------+
                                                |
                                                v
+---------------------------------------------------------------------------------------------------+
|                                 FLASK + SOCKET.IO BACKEND ENGINE                                  |
|  +----------------------------------------------------------------------------------------------+ |
|  | REST API Blueprints:                                                                         | |
|  | /auth, /buses, /routes, /stops, /trips, /tickets, /payments, /incidents, /alerts,            | |
|  | /maintenance, /fuel, /analytics, /simulation, /health, /docs                                | |
|  +----------------------------------------------------------------------------------------------+ |
|  | Domain Services:                                                                             | |
|  | GPSService, ETAService, TicketService, PaymentService, TripService, IncidentService          | |
|  +----------------------------------------------------------------------------------------------+ |
|  | Real-Time Ingestion & WebSocket Broadcasts:                                                   | |
|  | Telemetry ingestion, Kalman-style smoothing, geofencing, room subscriptions                  | |
|  +----------------------------------------------------------------------------------------------+ |
+-----------------------+-----------------------------------------------+---------------------------+
                        |                                               |
                        v                                               v
+-----------------------------------------------+   +-----------------------------------------------+
|           POSTGRESQL / SQLITE STORAGE         |   |                 REDIS CACHE                   |
| 30+ Normalized relational tables:             |   | - Live bus coordinate caching                 |
| Users, Buses, Routes, Stops, RouteStops,      |   | - Celery background task queues               |
| Schedules, Trips, Telemetries, Tickets,       |   | - Telemetry Pub/Sub broker                    |
| Payments, Incidents, WorkOrders, FuelLogs     |   +-----------------------------------------------+
+-----------------------------------------------+
```

## 2. Multi-Role RBAC Architecture
CityBus supports a strict Role-Based Access Control (RBAC) matrix for 9 distinct transit roles:
1. `passenger`: Search buses, plan journeys, purchase passes, view live ETA radar.
2. `driver`: Broadcast GPS telemetry, start/stop trips, log stop arrivals, trigger emergency SOS panic button.
3. `conductor`: Scan and cryptographically validate QR passes, maintain passenger headcounts.
4. `dispatcher`: Tactical 3-column command radar, live fleet tracking, direct driver messaging, emergency halt overrides.
5. `fleet_manager`: Vehicle asset management, fuel economy tracking, odometer logs.
6. `maintenance_manager`: Workshop work orders, parts inventory, downtime analytics.
7. `finance_manager`: Fare ledger, Razorpay sandbox transactions, refund approvals.
8. `admin`: Visual map route editor, stop geometry adjustments, user provisioning.
9. `super_admin`: Full system configuration, database diagnostics, security audit logs.
