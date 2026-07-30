import json

from flask import Blueprint, current_app

from utils.response import fail, ok

bhavnagar_bp = Blueprint("bhavnagar", __name__, url_prefix="/api/bhavnagar")

# Every top-level list in data/bhavnagar.json is exposed as its own endpoint,
# e.g. /api/bhavnagar/parks_and_gardens, /api/bhavnagar/police_stations, etc.
_SECTIONS = [
    "hospitals",
    "primary_health_centres",
    "government_offices",
    "municipal_offices",
    "fire_stations",
    "police_stations",
    "parks_and_gardens",
    "lakes_and_water_bodies",
    "tourist_places",
    "emergency_contacts",
    "nearby_ngos",
    "waste_collection_centers",
    "blood_banks",
    "ambulance_services",
    "public_toilets",
    "tree_plantation_areas",
    "environmental_projects",
    "rainwater_harvesting_sites",
    "smart_city_projects",
]


def _load_bhavnagar():
    try:
        with open(current_app.config["BHAVNAGAR_FILE"], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@bhavnagar_bp.route("/all", methods=["GET"])
def all_bhavnagar_data():
    """Everything in one call - handy for a city-overview page."""
    return ok("Bhavnagar city data fetched.", _load_bhavnagar())


@bhavnagar_bp.route("/sections", methods=["GET"])
def list_sections():
    return ok("Available Bhavnagar data sections.", _SECTIONS)


@bhavnagar_bp.route("/<string:section>", methods=["GET"])
def get_section(section):
    if section not in _SECTIONS:
        return fail(f"Unknown Bhavnagar data section '{section}'.", 404)
    data = _load_bhavnagar()
    return ok(f"{section} fetched.", data.get(section, []))
