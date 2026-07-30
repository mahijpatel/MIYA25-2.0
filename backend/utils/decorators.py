"""
Lightweight JWT middleware.

We avoid extra dependencies like flask-jwt-extended's full stack and instead
use PyJWT directly with two small decorators:

- @token_required        -> any logged-in user (citizen, gov, admin)
- @role_required("admin") -> only a specific role (or list of roles)

Both decorators NEVER raise unhandled exceptions - invalid/missing/expired
tokens always return a clean JSON error instead of crashing the request.
"""

from functools import wraps

import jwt
from flask import current_app, g, request

from utils.response import fail


def _extract_token():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()
    # also accept a raw token header for convenience during frontend dev
    return request.headers.get("x-access-token")


def _decode_token(token):
    secret = current_app.config["JWT_SECRET_KEY"]
    return jwt.decode(token, secret, algorithms=["HS256"])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_token()
        if not token:
            return fail("Authentication token is missing.", 401)
        try:
            payload = _decode_token(token)
        except jwt.ExpiredSignatureError:
            return fail("Session expired. Please log in again.", 401)
        except jwt.InvalidTokenError:
            return fail("Invalid authentication token.", 401)
        except Exception:
            return fail("Could not validate token.", 401)

        g.current_user = payload
        return f(*args, **kwargs)

    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = _extract_token()
            if not token:
                return fail("Authentication token is missing.", 401)
            try:
                payload = _decode_token(token)
            except jwt.ExpiredSignatureError:
                return fail("Session expired. Please log in again.", 401)
            except jwt.InvalidTokenError:
                return fail("Invalid authentication token.", 401)
            except Exception:
                return fail("Could not validate token.", 401)

            if payload.get("role") not in roles:
                return fail("You do not have permission to access this resource.", 403)

            g.current_user = payload
            return f(*args, **kwargs)

        return decorated

    return decorator


def optional_auth(f):
    """Attaches g.current_user if a valid token is present, but never blocks the request."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_token()
        g.current_user = None
        if token:
            try:
                g.current_user = _decode_token(token)
            except Exception:
                g.current_user = None
        return f(*args, **kwargs)

    return decorated
