import json

from flask import Blueprint, current_app

from utils.response import ok

hospital_bp = Blueprint("hospitals", __name__, url_prefix="/api")


def _load_bhavnagar():
    try:
        with open(current_app.config["BHAVNAGAR_FILE"], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@hospital_bp.route("/hospitals", methods=["GET"])
def list_hospitals():
    """Backs useHospitals()."""
    data = _load_bhavnagar()
    hospitals = data.get("hospitals", []) + data.get("primary_health_centres", [])
    return ok("Hospitals fetched.", hospitals)
