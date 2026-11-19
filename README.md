# Live Sports Scores & Odds Aggregator

A modular Flask backend built as a SaaS-style sports and betting odds aggregator powered by **The Odds API**, featuring **Redis** caching, dynamic API key management, per-key rate limiting, and a proactive background worker orchestrated via **Docker Compose**.

## Features & Architecture

* **Flask (Application Factory + Blueprints):** Clean separation of routes (`admin`, `odds`, `sports`) and core services (`auth`, `cache`, `limiter`, `sports_client`).
* **The Odds API Integration (`httpx`):** Fetches available sports, live/upcoming betting odds, and live/recent scores.
* **Redis Caching & Proactive Background Worker (`worker.py`):** Periodically syncs popular sport data into Redis in the background while keeping request-level caching to protect external API quotas and reduce latency.
* **Multi-Layer `X-API-Key` Authentication:** Supports static master keys from environment variables alongside dynamically generated and revocable keys stored in Redis.
* **Per-Key Rate Limiting (`Flask-Limiter`):** Enforces per-key request limits backed by Redis.
* **Docker Compose:** Runs `redis`, `web`, and `worker` services cleanly in isolated containers.

## Project Structure

```text
live-sports-aggregator/
├── app/
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── odds.py
│   │   └── sports.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cache.py
│   │   ├── limiter.py
│   │   └── sports_client.py
│   └── __init__.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
└── worker.py