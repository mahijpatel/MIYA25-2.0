"""
Plant identification prediction service.

Today this returns realistic dummy predictions (filename keyword matching,
falling back to a random plant from the catalog) so the frontend's
"Plant Identification" page always works end to end.

--------------------------------------------------------------------
HOW TO PLUG IN A REAL MODEL LATER
--------------------------------------------------------------------
Replace the body of `run_inference()` with real TensorFlow/Keras inference,
keeping the same function signature and the same return shape:

    {
        "name": str,
        "scientificName": str,
        "category": str,
        "medicinalUse": str,
        "emergencyUse": str,
        "note": str,
        "confidence": float (0-100),
    }

Everything else (the /predict route, JSON response format, uploads) stays
unchanged - only this function's internals need to change.
"""

import json
import os
import random

from flask import current_app


def _load_plants():
    path = current_app.config["PLANTS_FILE"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _plant_to_result(plant, confidence=None):
    return {
        "name": plant.get("name", "Unknown Plant"),
        "scientificName": plant.get("scientificName", ""),
        "category": plant.get("category", ""),
        "medicinalUse": plant.get("medicinalUse", ""),
        "emergencyUse": plant.get("emergencyUse", ""),
        "note": plant.get("precautions", "Traditional medicinal use only."),
        "confidence": confidence if confidence is not None else plant.get("confidenceExample", 92),
    }


def run_inference(filename: str):
    """
    Returns a PlantResult-shaped dict for the given uploaded filename.

    Current logic (placeholder for a real model):
      1. Lowercase the filename.
      2. If it contains a known plant's name (or a close keyword), return
         that plant with a high-confidence score.
      3. Otherwise return a random plant from the catalog with a
         realistic confidence score between 90 and 99.
    """
    plants = _load_plants()
    if not plants:
        # Absolute fallback so the endpoint never crashes even if the
        # data file is missing or corrupted.
        return {
            "name": "Tulsi",
            "scientificName": "Ocimum tenuiflorum",
            "category": "Herb",
            "medicinalUse": "Helps with cough, cold and sore throat.",
            "emergencyUse": "Chew washed leaves or prepare a warm infusion for mild cough.",
            "note": "Traditional medicinal use only.",
            "confidence": 96,
        }

    safe_name = (filename or "").lower()

    # keyword aliases -> catalog plant name, for common alternate spellings
    keyword_map = {
        "tulsi": "Tulsi",
        "basil": "Basil (Sweet Basil)",
        "neem": "Neem",
        "aloe": "Aloe Vera",
        "ashwagandha": "Ashwagandha",
        "giloy": "Giloy",
        "guduchi": "Guduchi (see Giloy)",
        "brahmi": "Brahmi",
        "amla": "Amla",
        "turmeric": "Turmeric",
        "haldi": "Turmeric",
        "ginger": "Ginger",
        "adrak": "Ginger",
        "mint": "Mint (Pudina)",
        "pudina": "Mint (Pudina)",
        "curry": "Curry Leaf",
        "lemongrass": "Lemongrass",
        "fenugreek": "Fenugreek (Methi)",
        "methi": "Fenugreek (Methi)",
        "hibiscus": "Hibiscus",
        "marigold": "Marigold (Genda)",
        "peepal": "Peepal",
        "banyan": "Banyan",
        "bael": "Bael",
        "shatavari": "Shatavari",
        "vasaka": "Vasaka (Adulsa)",
        "arjuna": "Arjuna",
        "sandalwood": "Sandalwood (Chandan)",
        "chandan": "Sandalwood (Chandan)",
        "henna": "Henna (Mehendi)",
        "mehendi": "Henna (Mehendi)",
        "coriander": "Coriander (Dhania)",
        "dhania": "Coriander (Dhania)",
        "cumin": "Cumin (Jeera)",
        "jeera": "Cumin (Jeera)",
        "fennel": "Fennel (Saunf)",
        "saunf": "Fennel (Saunf)",
        "clove": "Clove (Laung)",
        "laung": "Clove (Laung)",
        "cinnamon": "Cinnamon (Dalchini)",
        "dalchini": "Cinnamon (Dalchini)",
        "pepper": "Black Pepper (Kali Mirch)",
        "papaya": "Papaya Leaf",
        "moringa": "Moringa (Drumstick)",
        "drumstick": "Moringa (Drumstick)",
        "guava": "Guava Leaf",
        "vetiver": "Vetiver (Khus)",
        "khus": "Vetiver (Khus)",
        "kalmegh": "Kalmegh",
        "betel": "Betel Leaf (Paan)",
        "paan": "Betel Leaf (Paan)",
    }

    matched_plant = None
    for keyword, plant_name in keyword_map.items():
        if keyword in safe_name:
            matched_plant = next((p for p in plants if p["name"] == plant_name), None)
            if matched_plant:
                break

    if matched_plant:
        confidence = round(random.uniform(94, 99), 1)
        return _plant_to_result(matched_plant, confidence)

    # No keyword match -> pick a random plant, realistic confidence range
    random_plant = random.choice(plants)
    confidence = round(random.uniform(90, 99), 1)
    return _plant_to_result(random_plant, confidence)
