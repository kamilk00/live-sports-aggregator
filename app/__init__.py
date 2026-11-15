from flask import Flask, jsonify
from dotenv import load_dotenv
from app.services.limiter import limiter

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    # Initialize Flask-Limiter with the app
    limiter.init_app(app)

    # Register Blueprints
    from app.blueprints.sports import sports_bp
    from app.blueprints.odds import odds_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(sports_bp, url_prefix="/api/v1/sports")
    app.register_blueprint(odds_bp, url_prefix="/api/v1/odds")
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Rate Limit Exceeded",
            "detail": str(e.description)
        }), 429

    @app.route("/")
    def health_check():
        return jsonify({
            "service": "Live Sports Scores & Odds Aggregator",
            "version": "0.4.0",
            "status": "active"
        })

    return app