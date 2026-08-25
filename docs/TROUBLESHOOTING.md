# CityBus Enterprise Platform - Operational Troubleshooting Guide

## 1. Common Issues & Solutions

### A. SQLite Table Lock / Column Missing Error
- **Cause**: Schema changes on local development sqlite file without migrations.
- **Fix**: Re-seed database with fresh schema:
```bash
python backend/manage.py seed
```

### B. Geolocation Not Supported in Browser
- **Cause**: Insecure HTTP context or user blocked location permissions.
- **Fix**: Grant location permission in browser URL settings or test on `localhost` / HTTPS.

### C. Live Bus Marker Telemetry Delay
- **Cause**: GPS hardware sensor sleeping or WebSocket reconnecting.
- **Fix**: Check `health.html` diagnostics to verify Socket.IO stream and run `python backend/manage.py simulate` for simulated live GPS ticks.
