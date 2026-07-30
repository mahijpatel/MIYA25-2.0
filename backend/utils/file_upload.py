"""
Safe file upload helpers shared by profile photo, plant image and
complaint attachment uploads. Designed to never throw - callers get
a (success, filename_or_error) tuple back.
"""

import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def is_allowed_file(filename):
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file_storage, folder):
    """
    Saves an uploaded file into the given folder (must be one of the
    configured UPLOAD_FOLDER subfolders). Returns (True, filename) on
    success or (False, error_message) on failure. Never raises.
    """
    try:
        if file_storage is None or file_storage.filename == "":
            return False, "No file was provided."

        if not is_allowed_file(file_storage.filename):
            return False, "Unsupported file type. Allowed: jpg, jpeg, png, pdf."

        original_name = secure_filename(file_storage.filename)
        ext = original_name.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"

        os.makedirs(folder, exist_ok=True)
        destination = os.path.join(folder, unique_name)
        file_storage.save(destination)

        return True, unique_name
    except Exception as exc:  # noqa: BLE001 - deliberate catch-all, never crash
        return False, f"Could not save file: {exc}"
