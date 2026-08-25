"""
CityBus Enterprise Platform - Management CLI Tool (backend/manage.py)

Commands:
- python manage.py run          -> Runs Flask + Socket.IO server
- python manage.py seed         -> Seeds 50 buses, 20 routes, 300 stops, 1000 tickets
- python manage.py test         -> Executes automated test suites
- python manage.py simulate     -> Runs real-time GPS simulation background loop
"""

import sys
import os
import time

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import app, db
from seeds.seed_data import seed_enterprise_dataset
from services.simulator_service import simulator_engine


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py [run|seed|test|simulate]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == 'run':
        print("Starting CityBus Server on http://127.0.0.1:5000 ...")
        app.run(host='127.0.0.1', port=5000, debug=True)

    elif cmd == 'seed':
        with app.app_context():
            seed_enterprise_dataset()
            print("Database seeding completed.")

    elif cmd == 'test':
        import unittest
        print("Running CityBus Test Suite...")
        loader = unittest.TestLoader()
        tests_dir = os.path.join(os.path.dirname(backend_dir), 'tests')
        suite = loader.discover(tests_dir, pattern='test_*.py')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    elif cmd == 'simulate':
        print("Starting Headless Multi-Bus GPS Simulator Loop (Ctrl+C to stop)...")
        with app.app_context():
            while True:
                updated = simulator_engine.step_simulation()
                print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] Stepped {len(updated)} active municipal buses.")
                time.sleep(3)

    else:
        print(f"Unknown command: {cmd}")
        print("Valid commands: run, seed, test, simulate")


if __name__ == '__main__':
    from datetime import datetime
    main()
