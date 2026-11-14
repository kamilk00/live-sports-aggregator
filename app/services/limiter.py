import os
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STORAGE_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


def get_rate_limit_key() -> str:
    """
    Extract the API key from headers to enforce rate limiting per API key.
    Fall back to the remote IP address if no API key is present.
    """
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"key:{api_key}"
    return get_remote_address()


limiter = Limiter(
    key_func = get_rate_limit_key,
    storage_uri = REDIS_STORAGE_URL,
    default_limits = ["200 per day", "50 per hour"]
)