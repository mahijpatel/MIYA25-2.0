import json
import os

from flask import Blueprint, current_app, request

from services.prediction_service import run_inference
from utils.file_upload import save_upload
from utils.response import fail, ok

plant_bp = Blueprint("plants", __name__, url_prefix="/api")


def _load_plants():
    try:
        with open(current_app.config["PLANTS_FILE"], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


@plant_bp.route("/plants", methods=["GET"])
def list_plants():
    """Backs the useMedicinalPlants() hook - full catalog, optional search."""
    plants = _load_plants()
    search = (request.args.get("search") or "").strip().lower()
    category = (request.args.get("category") or "").strip().lower()

    if search:
        plants = [p for p in plants if search in p.get("name", "").lower()
                  or search in p.get("scientificName", "").lower()]
    if category:
        plants = [p for p in plants if p.get("category", "").lower() == category]

    return ok("Medicinal plants fetched.", plants)


@plant_bp.route("/plants/<string:name>", methods=["GET"])
def get_plant(name):
    plants = _load_plants()
    match = next((p for p in plants if p.get("name", "").lower() == name.lower()), None)
    if not match:
        return fail("Plant not found.", 404)
    return ok("Plant fetched.", match)


@plant_bp.route("/predict", methods=["POST"])
def predict():
    """
    Plant Identification page: accepts an uploaded image and returns a
    PlantResult. Uses filename-keyword matching today; see
    services/prediction_service.py for how to plug in a real model later.
    """
    try:
        if "image" not in request.files and "file" not in request.files:
            return fail("No image file was uploaded. Expected field 'image'.", 422)

        file_storage = request.files.get("image") or request.files.get("file")

        saved, saved_name_or_error = save_upload(file_storage, current_app.config["PLANT_IMAGE_FOLDER"])
        # Even if saving fails (e.g. disallowed type), we still try to run
        # inference off the original filename so the UI never breaks.
        original_filename = file_storage.filename if file_storage else ""

        result = run_inference(original_filename)

        response_data = dict(result)
        if saved:
            response_data["imageUrl"] = f"/uploads/plant_images/{saved_name_or_error}"
        else:
            response_data["imageUrl"] = ""
            response_data["uploadWarning"] = saved_name_or_error

        return ok("Plant identified successfully.", response_data)
    except Exception as exc:  # noqa: BLE001
        return fail(f"Could not identify plant: {exc}", 500)
