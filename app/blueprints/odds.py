from flask import Blueprint, jsonify
import json
from app.services.cache import redis_client, CACHE_TTL_SECONDS
from app.services.auth import verify_api_key
from app.services.limiter import limiter
from app.services.sports_client import fetch_odds_from_api, fetch_sports_from_api

odds_bp = Blueprint("odds", __name__)


@odds_bp.route("/available", methods=["GET"])
@verify_api_key
@limiter.limit("10 per minute")
def get_available_sports():
    """
    Fetch available sports list, backed by Redis cache and API key protection.
    """
    cache_key = "sports:available_list"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify({
            "source": "cache",
            "data": json.loads(cached_data)
        }), 200

    try:
        sports_data = fetch_sports_from_api()
        # Cache for a longer period since sport categories rarely change (e.g. 3600 seconds)
        redis_client.setex(cache_key, 3600, json.dumps(sports_data))

        return jsonify({
            "source": "the_odds_api",
            "data": sports_data
        }), 200
    except Exception as e:
        return jsonify({
            "error": "External API Error",
            "detail": str(e)
        }), 502


@odds_bp.route("/<sport_key>", methods=["GET"])
@verify_api_key
@limiter.limit("10 per minute")
def get_sport_odds(sport_key: str):
    """
    Fetch live betting odds for a given sport key, backed by Redis cache.
    """
    cache_key = f"odds:sport:{sport_key.lower()}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify({
            "source": "cache",
            "data": json.loads(cached_data)
        }), 200

    try:
        odds_data = fetch_odds_from_api(sport_key)
        # Cache sports odds with standard TTL to save API request quotas
        redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(odds_data))

        return jsonify({
            "source": "the_odds_api",
            "data": odds_data
        }), 200
    except Exception as e:
        return jsonify({
            "error": "External API Error",
            "detail": str(e)
        }), 502