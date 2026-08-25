"""
CityBus Enterprise Public Transportation Platform
Backend Configuration (backend/config.py)

Supports environment variables, PostgreSQL / SQLite dual persistence,
Redis caching & Celery broker, JWT authentication, and Razorpay sandbox credentials.
"""

import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'citybus-enterprise-secret-key-2026-secure'
    
    # Database Configuration (Defaults to local SQLite if DATABASE_URL not set)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'citybus.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    } if 'postgresql' in (os.environ.get('DATABASE_URL') or '') else {}

    # Redis & Celery
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379/0'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or REDIS_URL
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or REDIS_URL

    # JWT Authentication
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'citybus-jwt-token-secret-2026-enterprise-production-secure'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'

    # Razorpay Payment Gateway Sandbox (Test Mode)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'rzp_test_citybus_sandbox_key'
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'rzp_secret_citybus_test_2026'
    RAZORPAY_WEBHOOK_SECRET = os.environ.get('RAZORPAY_WEBHOOK_SECRET') or 'rzp_webhook_citybus_2026'

    # Security & CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    RATE_LIMIT_STORAGE_URL = os.environ.get('RATE_LIMIT_STORAGE_URL') or 'memory://'

    # Transit Operations Settings
    DEFAULT_CITY = "Vijayawada, Andhra Pradesh"
    STALE_GPS_THRESHOLD_SECONDS = 30
    DEFAULT_SPEED_LIMIT_KMH = 65.0
    GEOFENCE_RADIUS_METERS = 80.0
    BASE_FARE_INR = 15.0
    RATE_PER_KM_INR = 1.50

    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
