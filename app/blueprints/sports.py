from flask import Blueprint, jsonify
import json
from app.services.cache import redis_client, CACHE_TTL_SECONDS
from app.services.auth import verify_api_key
from app.services.limiter import limiter
from app.services.sports_client import fetch_scores_from_api

sports_bp = Blueprint("sports", __name__)


@sports_bp.route("/live/<sport_key>", methods=["GET"])
@verify_api_key
@limiter.limit("10 per minute")
def get_live_scores(sport_key: str):
    """
    Fetch live scores for a given sport key, backed by Redis cache, API key auth, and rate limiting.
    """
    cache_key = f"sports:scores:{sport_key.lower()}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify({
            "source": "cache",
            "data": json.loads(cached_data)
        }), 200

    try:
        scores_data = fetch_scores_from_api(sport_key)
        redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(scores_data))

        return jsonify({
            "source": "the_odds_api",
            "data": scores_data
        }), 200
    except Exception as e:
        return jsonify({
            "error": "External API Error",
            "detail": str(e)
        }), 502