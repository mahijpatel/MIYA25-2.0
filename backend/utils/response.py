"""
Standard response helpers so every endpoint returns the same JSON shape:

Success:
{ "success": true, "message": "...", "data": {} }

Error:
{ "success": false, "message": "..." }
"""

from flask import jsonify


def ok(message="Success", data=None, status=200):
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    else:
        payload["data"] = {}
    return jsonify(payload), status


def fail(message="Something went wrong", status=400, data=None):
    payload = {"success": False, "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status
