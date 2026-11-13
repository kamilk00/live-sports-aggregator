from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/status", methods = ["GET"])
def admin_status():
    return jsonify({"message": "Admin panel ready (v0.1.0)"}), 200