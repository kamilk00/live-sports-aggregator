from flask import Blueprint, jsonify

odds_bp = Blueprint("odds", __name__)


@odds_bp.route("/<sport_key>", methods = ["GET"])
def get_sport_odds(sport_key: str):
    return jsonify({
        "sport": sport_key,
        "message": "Odds endpoint ready (v0.1.0)"
    }), 200