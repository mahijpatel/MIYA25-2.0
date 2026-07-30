from datetime import datetime, timedelta

import jwt
from flask import Blueprint, current_app, g, request

from models import db
from models.user import User
from utils.decorators import token_required
from utils.response import fail, ok

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

VALID_ROLES = {"citizen", "gov", "admin"}


def _issue_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "name": user.name,
        "exp": datetime.utcnow() + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        body = request.get_json(silent=True) or {}
        name = (body.get("name") or "").strip()
        email = (body.get("email") or "").strip().lower()
        password = body.get("password") or ""
        role = body.get("role", "citizen")

        if role not in VALID_ROLES:
            role = "citizen"

        if not name or not email or not password:
            return fail("Name, email and password are required.", 422)

        if User.query.filter_by(email=email).first():
            return fail("An account with this email already exists.", 409)

        user = User(name=name, email=email, role=role, phone=body.get("phone", ""))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = _issue_token(user)
        return ok("Account created successfully.", {"token": token, "user": user.to_public_dict()}, 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Registration failed: {exc}", 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        body = request.get_json(silent=True) or {}
        email = (body.get("email") or "").strip().lower()
        password = body.get("password") or ""
        role = body.get("role")

        if not email or not password:
            return fail("Email and password are required.", 422)

        query = User.query.filter_by(email=email)
        if role in VALID_ROLES:
            query = query.filter_by(role=role)
        user = query.first()

        if not user or not user.check_password(password):
            return fail("Invalid email or password.", 401)

        if not user.is_active:
            return fail("This account has been deactivated.", 403)

        token = _issue_token(user)
        return ok("Login successful.", {"token": token, "user": user.to_public_dict()})
    except Exception as exc:  # noqa: BLE001
        return fail(f"Login failed: {exc}", 500)


@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    user = User.query.get(g.current_user["user_id"])
    if not user:
        return fail("User not found.", 404)
    return ok("Current user fetched.", user.to_public_dict())


@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    # Stateless JWT - logout is handled client-side by discarding the token.
    return ok("Logged out successfully.")
