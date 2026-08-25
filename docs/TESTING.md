# CityBus Enterprise Platform - Automated Testing Guide

## 1. Test Suite Structure
The testing suite is located in `tests/` and covers all critical business logic:
- `tests/test_auth.py`: Password hashing, JWT token lifecycle, login endpoint, and RBAC claims.
- `tests/test_buses.py`: Haversine distance formulas, live GPS ingestion, and proximity-sorted `/api/v1/buses/nearby` queries.
- `tests/test_tickets.py`: Fare rules, concessions, HMAC-SHA256 QR code signing, and validation state transitions (`VALID` -> `USED` -> `ALREADY_USED`).
- `tests/test_incidents.py`: Incident reporting, emergency panic button SOS escalation, and Kanban status updates.

## 2. Running Automated Tests
```bash
# Run all tests via management CLI
python backend/manage.py test

# Or run directly via unittest module
python -m unittest discover -s tests -p "test_*.py" -v
```
