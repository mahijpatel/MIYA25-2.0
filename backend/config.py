"""
Configuration for the MIYA25 backend.
All settings can be overridden with environment variables (see .env.example).
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "miya25-dev-secret-change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "miya25-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # --- Database (SQLite, lightweight, file based) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Uploads ---
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    PROFILE_PHOTO_FOLDER = os.path.join(UPLOAD_FOLDER, "profile_photos")
    PLANT_IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, "plant_images")
    COMPLAINT_ATTACHMENT_FOLDER = os.path.join(UPLOAD_FOLDER, "complaint_attachments")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}

    # --- CORS ---
    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",")

    # --- Data files (lightweight JSON "database" for reference data) ---
    DATA_DIR = os.path.join(BASE_DIR, "data")
    PLANTS_FILE = os.path.join(DATA_DIR, "plants.json")
    BHAVNAGAR_FILE = os.path.join(DATA_DIR, "bhavnagar.json")

    # --- Bhavnagar coordinates (used for live weather / AQI lookups) ---
    BHAVNAGAR_LAT = 21.7645
    BHAVNAGAR_LON = 72.1519

    # --- External APIs (free, no key required) ---
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
    AQI_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
    EXTERNAL_API_TIMEOUT = 5  # seconds - fail fast, fall back to dummy data
