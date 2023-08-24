"""Flask Application Entry Point."""

from flask import Flask
from flask_cors import CORS

from api.exceptions import handler
from api.model import db
from api.routes import init_routes
from config import Settings


def create_app() -> Flask:
    """Initialize and setup flask app.

    Returns: Flask Application
    """
    app = Flask(__name__)

    with app.app_context():
        app.config.update(Settings())
        CORS(app)
        init_routes(app)
        db.init_app(app)
        db.create_all()
        handler.register_error_handlers(app)

    return app


if __name__ == "__main__":
    create_app().run()
