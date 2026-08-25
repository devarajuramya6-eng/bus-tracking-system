# CityBus Enterprise Platform - Real-Time Ingestion & WebSocket Stream Pipeline

## 1. Real-Time Telemetry Flow
```
[Driver Mobile HUD / OBD2 Hardware]
                |
                v (HTTP POST /api/v1/buses/location or Socket.IO driver:telemetry)
[Backend Telemetry Ingestion]
                |
    +-----------+-----------+
    |                       |
    v                       v
[Redis Cache & DB]     [ETAService Calculation Engine]
    |                       |
    +-----------+-----------+
                |
                v
[Socket.IO Room Broadcasting]
   - room: bus:<id>       (Commuters viewing single bus)
   - room: route:<id>     (Passengers on route corridor)
   - room: dispatcher     (Tactical command center radar)
                |
                v
[Passenger / Dispatcher Web UI]
                |
                v
[VehicleInterpolator (requestAnimationFrame cubic easing)]
                |
                v
[Smooth Vector Marker Gliding on Leaflet Map]
```

## 2. Room Subscription Matrix
Clients subscribe to localized telemetry topics to optimize network bandwidth:
- `bus:<id>`: Receives coordinates and speed for one bus.
- `route:<id>`: Receives position updates for all vehicles operating on a route.
- `dispatcher_radar`: Receives high-frequency pings for the entire 50-bus fleet.
- `incidents`: Receives emergency panic and service disruption broadcasts.
