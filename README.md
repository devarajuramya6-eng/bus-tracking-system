# CityBus — Enterprise Intelligent Public Transportation Platform

> **A Complete Commercial-Grade Real-Time Municipal Public Transit Management Platform** for commuters, drivers, conductors, tactical dispatchers, and transit authorities in the **Vijayawada & Amaravati Capital Region, Andhra Pradesh**.

---

## 🌟 Executive Summary

**CityBus** is a comprehensive, production-grade transit intelligence platform built from the ground up to replace outdated legacy transit prototypes with an 80,000+ LOC enterprise architecture. It delivers real-time sub-second vehicle telemetry, dynamic ETA forecasting, contactless cryptographic QR pass validation, Razorpay test payment checkout, tactical dispatch radar, visual map route design, and maintenance work order management.

---

## 🚀 Key Features by Role & Domain

### 1. 🧑‍💼 Commuters & Passengers
- **Interactive Fullscreen Radar Map**: Live gliding bus markers powered by cubic easing interpolation, heading rotation arrows, and stop popups.
- **Dynamic Arrival ETAs**: Kinematics-based arrival time predictions factoring in vehicle speed, corridor geometry, peak hour traffic multipliers ($1.25\times$), and stop dwell times.
- **Intermodal Journey Planner**: Point-to-point transit routing with walking directions, transfer segments, and fare estimation.
- **Contactless QR Ticketing**: Book passes online with instant HMAC-SHA256 cryptographically signed QR tokens in a digital pass wallet with refund processing.
- **OmniSearch & Command Palette**: Instant keyboard navigation (`Ctrl + K`) across all 50 buses, 20 routes, 300 stops, and operational tools.

### 2. 🚌 Drivers & Operators
- **High-Contrast Cockpit HUD**: Touch-friendly gauges for live velocity, GPS coordinates, passenger headcount, and route progression.
- **GPS Telemetry Broadcaster**: Dual hardware sensor watch stream with fallback kinematic simulator.
- **Emergency SOS Panic Button**: 1-click critical priority escalation broadcasting coordinates immediately to dispatch radar.

### 3. 🎫 Conductors & Fare Collection
- **Mobile POS & Camera QR Scanner**: High-speed QR scanning verifying cryptographic signatures against fraud, ticket reuse (`ALREADY_USED`), and expiration.
- **Passenger Headcount Tracker**: Real-time boarding and alighting counter synchronizing bus occupancy to live maps.

### 4. 🛰️ Tactical Dispatchers
- **3-Column Tactical Command Radar**: Real-time fleet roster with status filters (`Moving`, `Delayed`, `Offline`, `Emergency`), central radar map, and vehicle directive control panel.
- **Direct Messaging & Emergency Overrides**: Send cockpit HUD advisories or issue mandatory halt directives to drivers.

### 5. 🏢 Operations & Enterprise Administration
- **Visual Map Route Editor**: Interactive map canvas to draw route corridor polylines, position stops, and compute corridor runtime/distance.
- **Drag-and-Drop Incident Kanban**: Multi-stage incident resolution workflow (`New` ➔ `Acknowledged` ➔ `In Progress` ➔ `Resolved`).
- **Preventive Maintenance Bay**: Work order lifecycle, odometer readings, downtime hours, and spare parts logs.
- **Fleet Fuel Economy Ledger**: Pump station refills, cost per liter, and vehicle comparative efficiency charts (km/L).
- **Executive Analytics**: Real-time KPI summary cards, weekly ridership line charts, On-Time Performance (OTP) trends, and fleet availability donuts.
- **Node & Diagnostics Health**: Liveness and readiness diagnostic probes (`/health`, `/health/live`, `/health/ready`).

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend Core** | Semantic HTML5, Vanilla JavaScript (ES6+ Modules), CSS3 Enterprise Custom Properties (Tokens), Carto & OpenStreetMap Tiles, Leaflet.js |
| **Backend Engine** | Python 3.10+, Flask Application Factory, Flask-CORS, Flask-SocketIO |
| **Database & Persistence** | PostgreSQL with PostGIS Spatial Extensions (Production) / SQLite (Local Standalone), SQLAlchemy ORM |
| **Caching & Messaging** | Redis Cache & Pub/Sub, Celery Background Workers |
| **Security & Auth** | JWT Access (8h) & Refresh (30d) Tokens, HMAC-SHA256 QR Signatures, RBAC 9-Role Access Control Matrix |
| **Payments** | Razorpay Test Sandbox Order & HMAC Verification Flow |
| **Containerization** | Docker Multi-Stage Build, Docker Compose, Nginx Reverse Proxy |

---

## 🚦 Quick Start Guide

### Prerequisites
- Python 3.10 or higher
- pip package manager

### 1. Clone & Setup
```bash
cd "c:/Users/HP/OneDrive/Desktop/new bus/Bus"
pip install -r requirements.txt
```

### 2. Seed Enterprise Transit Dataset
Seeds 50 operating buses, 50 drivers, 20 conductors, 20 routes, 300 stops, 500 trips, 1,000 tickets, payments, incidents, and maintenance logs:
```bash
python backend/manage.py seed
```

### 3. Run Automated Test Suite
Executes the comprehensive automated unit test suite:
```bash
python backend/manage.py test
```

### 4. Start the Application Server
```bash
python backend/manage.py run
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🔑 Demo Sandbox Credentials (All 9 Roles)

| Role | Email | Password | Primary Workspace |
|---|---|---|---|
| **Passenger** | `passenger@citybus.transit` | `citybus2026` | `index.html`, `passenger-map.html`, `tickets.html` |
| **Driver** | `ravi@citybus.transit` | `citybus2026` | `driver.html` (Cockpit HUD) |
| **Conductor** | `conductor@citybus.transit` | `citybus2026` | `conductor.html` (Camera POS) |
| **Dispatcher** | `dispatcher@citybus.transit` | `citybus2026` | `dispatcher.html` (Command Radar) |
| **Fleet Manager** | `fleet@citybus.transit` | `citybus2026` | `fuel.html`, `admin.html` |
| **Maintenance Mgr** | `maintenance@citybus.transit` | `citybus2026` | `maintenance.html` |
| **Finance Manager** | `finance@citybus.transit` | `citybus2026` | `analytics.html` |
| **Admin** | `admin@citybus.transit` | `citybus2026` | `admin.html`, `incidents.html` |
| **Super Admin** | `superadmin@citybus.transit` | `citybus2026` | `health.html`, `simulation.html` |

*(You can also use the 1-click role buttons on `login.html` to log in instantly).*

---

## 📚 Technical Documentation Suite

Complete technical documentation is available in the `docs/` directory:
- [Architecture & RBAC Matrix](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/ARCHITECTURE.md)
- [REST & WebSocket API Reference](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/API.md)
- [3NF Database Schema & ERD](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/DATABASE.md)
- [GPS Pipeline & Spatial Engineering](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/GPS.md)
- [Real-Time WebSocket Streams](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/REALTIME.md)
- [Dynamic ETA Forecasting Model](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/ETA.md)
- [Digital Ticketing & QR Cryptography](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/TICKETING.md)
- [Payment Gateway Integration](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/PAYMENTS.md)
- [Deployment & Docker Guide](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/DEPLOYMENT.md)
- [Security & Threat Model](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/SECURITY.md)
- [Automated Testing Guide](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/TESTING.md)
- [Operational Troubleshooting](file:///c:/Users/HP/OneDrive/Desktop/new%20bus/Bus/docs/TROUBLESHOOTING.md)

---

&copy; 2026 CityBus Enterprise Platform. All rights reserved.

<!-- feature/transit-core update -->

<!-- feature/realtime-gps update -->
