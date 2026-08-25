# CityBus Enterprise Platform - Deployment & Infrastructure Guide

## 1. Quick Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed database (50 buses, 20 routes, 300 stops, 1000 tickets)
python backend/manage.py seed

# 3. Run unit test suite
python backend/manage.py test

# 4. Start local Flask + Socket.IO server
python backend/manage.py run
```
Open `http://127.0.0.1:5000` in any modern web browser.

## 2. Docker & Multi-Container Production Stack
```bash
# Build and run the entire stack (Flask, PostgreSQL + PostGIS, Redis, Nginx)
docker-compose up -d --build

# Run database migrations / seeder inside container
docker-compose exec web python backend/manage.py seed

# View real-time cluster logs
docker-compose logs -f
```

## 3. Environment Variables Reference
| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL or SQLite connection string | `sqlite:///backend/citybus.db` |
| `REDIS_URL` | Redis cache and message broker URL | `redis://127.0.0.1:6379/0` |
| `SECRET_KEY` | Flask session and HMAC cryptography key | `<SET_IN_ENVIRONMENT>` |
| `JWT_SECRET_KEY` | 32+ character JWT signing key | `<SET_IN_ENVIRONMENT>` |
| `RAZORPAY_KEY_ID` | Razorpay API sandbox key ID | `<SET_IN_ENVIRONMENT>` |
| `RAZORPAY_KEY_SECRET` | Razorpay API sandbox secret | `<SET_IN_ENVIRONMENT>` |
