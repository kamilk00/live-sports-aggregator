from flask import Blueprint, jsonify
import json
from app.services.cache import redis_client, CACHE_TTL_SECONDS
from app.services.auth import verify_api_key
from app.services.limiter import limiter

sports_bp = Blueprint("sports", __name__)


@sports_bp.route("/live", methods=["GET"])
@verify_api_key
@limiter.limit("10 per minute")
def get_live_scores():
    """
    Fetch live scores, backed by Redis cache, API key auth, and per-key rate limiting.
    """
    cache_key = "sports:scores:live"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify({
            "source": "cache",
            "data": json.loads(cached_data)
        }), 200

    live_matches = [
        {"match_id": 101, "home_team": "Real Madrid", "away_team": "FC Barcelona", "score": "2:1", "minute": 74},
        {"match_id": 102, "home_team": "Arsenal", "away_team": "Manchester City", "score": "0:0", "minute": 32}
    ]

    redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(live_matches))

    return jsonify({
        "source": "external_api",
        "data": live_matches
    }), 200