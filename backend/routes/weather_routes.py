"""
Weather and Air Quality routes for the /citizen/weather and /citizen/aqi pages.

Tries a real, free, no-API-key lookup (Open-Meteo) for Bhavnagar's
coordinates. If the request fails for any reason (no internet on the
server, rate limiting, etc.) it falls back to realistic dummy data so
the frontend never breaks.
"""

import requests
from flask import Blueprint, current_app

from utils.response import ok

weather_bp = Blueprint("weather", __name__, url_prefix="/api")


def _fallback_weather():
    return {
        "source": "fallback",
        "city": "Bhavnagar",
        "temperature_c": 33.0,
        "feels_like_c": 36.0,
        "humidity_percent": 62,
        "wind_kmph": 14.0,
        "condition": "Partly Cloudy",
        "forecast": [
            {"day": "Today", "high_c": 34, "low_c": 27, "condition": "Partly Cloudy"},
            {"day": "Tomorrow", "high_c": 35, "low_c": 27, "condition": "Sunny"},
            {"day": "Day 3", "high_c": 33, "low_c": 26, "condition": "Humid"},
        ],
    }


def _fallback_aqi():
    return {
        "source": "fallback",
        "city": "Bhavnagar",
        "aqi": 82,
        "category": "Moderate",
        "pm2_5": 34.5,
        "pm10": 58.2,
        "advisory": "Air quality is acceptable; unusually sensitive people should consider limiting prolonged outdoor exertion.",
    }


@weather_bp.route("/weather", methods=["GET"])
def get_weather():
    """Backs useWeather()."""
    lat = current_app.config["BHAVNAGAR_LAT"]
    lon = current_app.config["BHAVNAGAR_LON"]
    timeout = current_app.config["EXTERNAL_API_TIMEOUT"]

    try:
        response = requests.get(
            current_app.config["WEATHER_API_URL"],
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,apparent_temperature",
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": "Asia/Kolkata",
                "forecast_days": 3,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        raw = response.json()
        current = raw.get("current", {})
        daily = raw.get("daily", {})

        forecast = []
        days = daily.get("time", [])
        highs = daily.get("temperature_2m_max", [])
        lows = daily.get("temperature_2m_min", [])
        for i, day in enumerate(days):
            forecast.append(
                {
                    "day": day,
                    "high_c": highs[i] if i < len(highs) else None,
                    "low_c": lows[i] if i < len(lows) else None,
                    "condition": "See forecast",
                }
            )

        data = {
            "source": "open-meteo",
            "city": "Bhavnagar",
            "temperature_c": current.get("temperature_2m"),
            "feels_like_c": current.get("apparent_temperature"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_kmph": current.get("wind_speed_10m"),
            "condition": "Live data",
            "forecast": forecast or _fallback_weather()["forecast"],
        }
        return ok("Weather fetched.", data)
    except Exception:
        return ok("Weather fetched (offline fallback).", _fallback_weather())


@weather_bp.route("/aqi", methods=["GET"])
def get_aqi():
    """Backs the AQI page."""
    lat = current_app.config["BHAVNAGAR_LAT"]
    lon = current_app.config["BHAVNAGAR_LON"]
    timeout = current_app.config["EXTERNAL_API_TIMEOUT"]

    try:
        response = requests.get(
            current_app.config["AQI_API_URL"],
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "us_aqi,pm2_5,pm10",
                "timezone": "Asia/Kolkata",
            },
            timeout=timeout,
        )
        response.raise_for_status()
        raw = response.json()
        current = raw.get("current", {})
        aqi_value = current.get("us_aqi")

        category = "Unknown"
        if isinstance(aqi_value, (int, float)):
            if aqi_value <= 50:
                category = "Good"
            elif aqi_value <= 100:
                category = "Moderate"
            elif aqi_value <= 150:
                category = "Unhealthy for Sensitive Groups"
            elif aqi_value <= 200:
                category = "Unhealthy"
            else:
                category = "Very Unhealthy"

        data = {
            "source": "open-meteo",
            "city": "Bhavnagar",
            "aqi": aqi_value,
            "category": category,
            "pm2_5": current.get("pm2_5"),
            "pm10": current.get("pm10"),
            "advisory": "Live reading from Open-Meteo Air Quality API.",
        }
        return ok("Air quality fetched.", data)
    except Exception:
        return ok("Air quality fetched (offline fallback).", _fallback_aqi())
