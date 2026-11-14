from flask import Blueprint, jsonify, request
from app.services.auth import verify_api_key, generate_api_key, revoke_api_key

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/generate-key", methods=["POST"])
@verify_api_key
def create_api_key():
    """
    Admin endpoint to dynamically generate and store a new active API key in Redis.
    """
    data = request.get_json() or {}
    client_name = data.get("client_name")

    if not client_name:
        return jsonify({"error": "Bad Request", "detail": "Missing 'client_name' in request body."}), 400

    new_key = generate_api_key(client_name)
    return jsonify({
        "client_name": client_name,
        "api_key": new_key,
        "message": "Store this key safely. It will not be shown again."
    }), 201


@admin_bp.route("/revoke-key", methods=["POST"])
@verify_api_key
def disable_api_key():
    """
    Admin endpoint to revoke/deactivate an existing API key immediately.
    """
    data = request.get_json() or {}
    api_key = data.get("api_key")

    if not api_key:
        return jsonify({"error": "Bad Request", "detail": "Missing 'api_key' in request body."}), 400

    success = revoke_api_key(api_key)
    if not success:
        return jsonify({"error": "Not Found", "detail": "API key not found in Redis store."}), 404

    return jsonify({
        "api_key": api_key,
        "status": "revoked",
        "message": "API key has been successfully deactivated."
    }), 200