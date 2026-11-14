from flask import Blueprint, jsonify
from app.services.auth import verify_api_key
from app.services.limiter import limiter

odds_bp = Blueprint("odds", __name__)


@odds_bp.route("/<sport_key>", methods=["GET"])
@verify_api_key
@limiter.limit("10 per minute")
def get_sport_odds(sport_key: str):
    """
    Fetch betting odds for a given sport with auth and rate limiting.
    """
    return jsonify({
        "sport": sport_key.lower(),
        "source": "mock_odds_api",
        "odds": [
            {"bookmaker": "Bet365", "home_win": 1.95, "draw": 3.40, "away_win": 3.80}
        ]
    }), 200