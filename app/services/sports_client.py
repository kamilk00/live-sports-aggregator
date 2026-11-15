import os
import httpx

ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"


def fetch_sports_from_api() -> list:
    """
    Fetch available sports list from The Odds API.
    """
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        raise ValueError("ODDS_API_KEY is not configured in environment variables.")

    url = f"{ODDS_API_BASE_URL}/sports"
    params = {
        "apiKey": api_key
    }

    with httpx.Client() as client:
        response = client.get(url, params = params)
        response.raise_for_status()
        return response.json()


def fetch_odds_from_api(sport_key: str) -> list:
    """
    Fetch live betting odds for a specific sport key from The Odds API.
    """
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        raise ValueError("ODDS_API_KEY is not configured in environment variables.")

    url = f"{ODDS_API_BASE_URL}/sports/{sport_key}/odds"
    params = {
        "apiKey": api_key,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    with httpx.Client() as client:
        response = client.get(url, params = params)
        response.raise_for_status()
        return response.json()