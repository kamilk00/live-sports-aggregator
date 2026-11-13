from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    # Rejestracja Blueprintów
    from app.blueprints.sports import sports_bp
    from app.blueprints.odds import odds_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(sports_bp, url_prefix = "/api/v1/sports")
    app.register_blueprint(odds_bp, url_prefix = "/api/v1/odds")
    app.register_blueprint(admin_bp, url_prefix = "/api/v1/admin")

    @app.route("/")
    def health_check():
        return jsonify({
            "service": "Live Sports Scores & Odds Aggregator",
            "version": "0.1.0",
            "status": "active"
        })

    return app