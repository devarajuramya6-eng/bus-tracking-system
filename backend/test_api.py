"""
CityBus - Backend Test & Verification Script (test_api.py)

Runs automated tests against all API endpoints using Flask test client.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app


def test_citybus_backend():
    client = app.test_client()
    passed = 0
    total = 0

    def check(name, response, expected_status=200, check_fn=None):
        nonlocal passed, total
        total += 1
        data = response.get_json()
        status_ok = response.status_code == expected_status
        content_ok = check_fn(data) if check_fn else True

        if status_ok and content_ok:
            print(f"  [PASS] {name} (Status {response.status_code})")
            passed += 1
        else:
            print(f"  [FAIL] {name} (Status {response.status_code}, Response: {data})")

    print("\n" + "=" * 60)
    print("Running CityBus Flask API Verification Tests")
    print("=" * 60)

    # 1. Root Documentation Endpoint
    r = client.get('/')
    check("GET / (Root API Info)", r, 200, lambda d: "endpoints" in d and d["status"] == "Online")

    # 2. Get All Buses
    r = client.get('/api/buses')
    check("GET /api/buses", r, 200, lambda d: d["success"] and len(d["buses"]) >= 10)

    # 3. Get Single Bus
    r = client.get('/api/buses/1')
    check("GET /api/buses/1", r, 200, lambda d: d["success"] and d["bus"]["bus_number"] == "27A")

    # 4. Get Non-existent Bus
    r = client.get('/api/buses/9999')
    check("GET /api/buses/9999 (404 check)", r, 404, lambda d: not d["success"])

    # 5. Get All Routes
    r = client.get('/api/routes')
    check("GET /api/routes", r, 200, lambda d: d["success"] and len(d["routes"]) >= 5)

    # 6. Get Single Route with Stops
    r = client.get('/api/routes/1')
    check("GET /api/routes/1", r, 200, lambda d: d["success"] and len(d["route"]["stops"]) >= 7)

    # 7. Get Stops
    r = client.get('/api/stops')
    check("GET /api/stops", r, 200, lambda d: d["success"] and len(d["stops"]) >= 15)

    # 8. Get Nearby Buses (Vijayawada Benz Circle Coordinates)
    r = client.get('/api/buses/nearby?lat=16.5062&lng=80.6480')
    check("GET /api/buses/nearby?lat=16.5062&lng=80.6480", r, 200, lambda d: d["success"] and len(d["buses"]) > 0 and "distance_km" in d["buses"][0])

    # 9. Update Bus GPS Location
    r = client.post('/api/buses/location', json={
        "bus_id": 1,
        "latitude": 16.5072,
        "longitude": 80.6490,
        "speed": 35.5
    })
    check("POST /api/buses/location", r, 200, lambda d: d["success"] and d["bus_id"] == 1)

    # 10. Start Trip
    r = client.post('/api/trips/start', json={
        "bus_id": 1,
        "driver_id": 1,
        "route_id": 1
    })
    trip_id = r.get_json().get("trip_id") if r.status_code == 201 else None
    check("POST /api/trips/start", r, 201, lambda d: d["success"] and "trip_id" in d)

    # 11. Stop Trip
    r = client.post('/api/trips/stop', json={
        "trip_id": trip_id or 1,
        "bus_id": 1
    })
    check("POST /api/trips/stop", r, 200, lambda d: d["success"])

    # 12. Login (Success)
    r = client.post('/api/login', json={
        "email": "ravi@citybus.transit",
        "password": "citybus2026"
    })
    check("POST /api/login (Valid Driver)", r, 200, lambda d: d["success"] and d["user"]["role"] == "driver")

    # 13. Login (Invalid Credentials)
    r = client.post('/api/login', json={
        "email": "ravi@citybus.transit",
        "password": "wrongpassword"
    })
    check("POST /api/login (Invalid Password)", r, 401, lambda d: not d["success"])

    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed successfully!")
    print("=" * 60 + "\n")

    if passed == total:
        print("ALL API ENDPOINTS ARE WORKING PERFECTLY!\n")
    else:
        sys.exit(1)


if __name__ == '__main__':
    test_citybus_backend()
