import os
import secrets
from functools import wraps
from flask import request, jsonify
from app.services.cache import redis_client

API_KEY_HEADER_NAME = "X-API-Key"


def verify_api_key(f):
    """
    Decorator to validate the provided X-API-Key against environment variables and Redis.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get(API_KEY_HEADER_NAME)

        if not api_key:
            return jsonify({
                "error": "Unauthorized",
                "detail": "Missing API Key. Provide 'X-API-Key' header."
            }), 401

        # Check environment variables for legacy keys
        raw_keys = os.getenv("API_KEYS", "")
        allowed_keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
        if api_key in allowed_keys:
            return f(*args, **kwargs)

        # Check dynamic keys stored in Redis
        redis_key = f"apikey:{api_key}"
        key_data = redis_client.hgetall(redis_key)

        if not key_data or key_data.get("status") != "active":
            return jsonify({
                "error": "Forbidden",
                "detail": "Invalid or inactive/revoked API Key provided."
            }), 403

        return f(*args, **kwargs)

    return decorated_function


def generate_api_key(client_name: str) -> str:
    """
    Generate a secure random API key and store it in Redis associated with a client name.
    """
    random_token = secrets.token_hex(32)
    api_key = f"ftf_live_{random_token}"
    
    redis_key = f"apikey:{api_key}"
    redis_client.hset(redis_key, mapping = {
        "client_name": client_name,
        "status": "active"
    })
    
    return api_key


def revoke_api_key(api_key: str) -> bool:
    """
    Revoke an active API key by changing its status to 'revoked' in Redis.
    """
    redis_key = f"apikey:{api_key}"
    key_data = redis_client.hgetall(redis_key)
    
    if not key_data:
        return False
        
    redis_client.hset(redis_key, "status", "revoked")
    return True