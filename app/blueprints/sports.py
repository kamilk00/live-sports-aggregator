from flask import Blueprint, jsonify

sports_bp = Blueprint("sports", __name__)


@sports_bp.route("/live", methods = ["GET"])
def get_live_scores():
    return jsonify({"message": "Live scores endpoint ready (v0.1.0)"}), 200