# CityBus Enterprise Platform - REST & WebSocket API Specification

## 1. Authentication Endpoints (`/api/v1/auth`)
- `POST /api/v1/auth/login`: Authenticates credentials and returns JWT Access & Refresh tokens.
- `POST /api/v1/auth/register`: Creates a new passenger account.
- `POST /api/v1/auth/refresh`: Refreshes expired access tokens.
- `GET /api/v1/auth/me`: Fetches profile of currently authenticated user.

## 2. Bus Fleet Endpoints (`/api/v1/buses`)
- `GET /api/v1/buses`: Lists all municipal buses with optional `status` filter.
- `GET /api/v1/buses/{id}`: Returns single bus details with dynamic computed ETA.
- `GET /api/v1/buses/nearby?lat={lat}&lng={lng}&radius_km={radius}`: Returns proximity-sorted buses.
- `POST /api/v1/buses/location`: Ingests real-time GPS telemetry from driver device or OBD2 tracker.

## 3. Routes & Stops (`/api/v1/routes`, `/api/v1/stops`)
- `GET /api/v1/routes`: Returns all active transit corridors.
- `GET /api/v1/routes/{id}`: Returns complete corridor with ordered stop sequence and waypoints.
- `GET /api/v1/stops`: Returns city stops with accessibility amenities.
- `GET /api/v1/stops/{id}`: Returns single stop and upcoming arrivals.

## 4. Trips & Operations (`/api/v1/trips`)
- `GET /api/v1/trips`: Lists active and historical trips.
- `POST /api/v1/trips/start`: Starts driver trip lifecycle.
- `POST /api/v1/trips/stop`: Concludes trip and marks vehicle offline.

## 5. Ticketing & Payments (`/api/v1/tickets`, `/api/v1/payments`)
- `POST /api/v1/tickets`: Books ticket and creates HMAC-SHA256 signed QR code.
- `POST /api/v1/tickets/validate`: Validates scanned QR token on conductor terminal.
- `GET /api/v1/tickets/user/{userId}`: Returns passenger digital wallet history.
- `POST /api/v1/payments/order`: Creates Razorpay checkout order.
- `POST /api/v1/payments/verify`: Validates HMAC signature and marks payment SUCCESS.

## 6. Incidents & Emergency SOS (`/api/v1/incidents`)
- `GET /api/v1/incidents`: Lists incidents with status filter.
- `POST /api/v1/incidents`: Reports breakdown, traffic delay, or medical incident.
- `POST /api/v1/incidents/emergency/sos`: Broadcasts Priority-1 Emergency SOS to dispatch command.
- `PATCH /api/v1/incidents/{id}/status`: Transitions incident through Kanban states.

## 7. Diagnostics & Health (`/health`)
- `GET /health`: Basic health check.
- `GET /health/live`: Liveness probe.
- `GET /health/ready`: Readiness probe verifying database and fleet connectivity.
