# CityBus Enterprise Platform - GPS Pipeline & Spatial Engineering

## 1. High-Frequency Telemetry Ingestion
CityBus ingests real-time GPS telemetry from hardware OBD-II devices and driver mobile browser sensors:
- Endpoint: `POST /api/v1/buses/location`
- Frequency: 2-3 seconds per active vehicle.
- Fields: `latitude`, `longitude`, `speed`, `heading`, `accuracy`.

## 2. Heading Angle Calculation
When heading is omitted by device GPS sensors, the engine calculates the bearing angle $\theta$ relative to True North using forward spherical trigonometry:

$$\theta = \text{atan2}\Big(\sin(\Delta \lambda) \cdot \cos(\phi_2), \cos(\phi_1) \cdot \sin(\phi_2) - \sin(\phi_1) \cdot \cos(\phi_2) \cdot \cos(\Delta \lambda)\Big)$$

The angle is normalized to $[0^\circ, 360^\circ)$ and rendered on Leaflet vector markers.

## 3. Spatial Geofencing & Stop Arrival Detection
The backend evaluates circular bounding geofences around each ordered route stop (default radius: 80 meters) using the Great-Circle Haversine distance:

$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$

When a vehicle breaches the 80m perimeter, a stop arrival event is logged and propagated to ETA computation nodes.
