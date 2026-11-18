import os
import time
import json
import logging
from dotenv import load_dotenv
from app.services.cache import redis_client
from app.services.sports_client import fetch_scores_from_api, fetch_odds_from_api

load_dotenv()

logging.basicConfig(level = logging.INFO, format = "%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Popular sport keys to prefetch
POPULAR_SPORTS = ["soccer_epl", "soccer_spain_la_liga"]
FETCH_INTERVAL_SECONDS = 60


def background_sync():
    """
    Periodically fetch fresh data from external API and update Redis cache proactively.
    """
    logger.info("Starting background sync worker...")

    while True:
        for sport_key in POPULAR_SPORTS:
            logger.info(f"Syncing data for sport: {sport_key}")
            
            # Sync live scores
            try:
                scores_data = fetch_scores_from_api(sport_key)
                scores_cache_key = f"sports:scores:{sport_key.lower()}"
                redis_client.set(scores_cache_key, json.dumps(scores_data))
                logger.info(f"Successfully updated live scores cache for {sport_key}")
            except Exception as e:
                logger.error(f"Failed to sync scores for {sport_key}: {e}")

            # Sync odds
            try:
                odds_data = fetch_odds_from_api(sport_key)
                odds_cache_key = f"odds:sport:{sport_key.lower()}"
                redis_client.set(odds_cache_key, json.dumps(odds_data))
                logger.info(f"Successfully updated odds cache for {sport_key}")
            except Exception as e:
                logger.error(f"Failed to sync odds for {sport_key}: {e}")

            # Sleep briefly between requests to respect rate limits
            time.sleep(5)

        logger.info(f"Sync cycle completed. Sleeping for {FETCH_INTERVAL_SECONDS} seconds...")
        time.sleep(FETCH_INTERVAL_SECONDS)


if __name__ == "__main__":
    background_sync()