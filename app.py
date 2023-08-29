"""Flask Application Entry Point."""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

from api.exceptions import handler
from api.model import db
from api.routes import init_routes
from api.schedulers.auto_sign import setup_schedulers
from config import Settings


def create_app() -> Flask:  # sourcery skip: extract-method
    """Initialize and setup flask app.

    Returns: Flask Application
    """
    app = Flask(__name__)

    with app.app_context():
        app.config.update(Settings())
        CORS(app)
        init_routes(app)
        db.init_app(app)
        Migrate(app, db)
        db.create_all()
        handler.register_error_handlers(app)

        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.api_enabled = True
        setup_schedulers(app, scheduler)
        scheduler.start()

    return app


if __name__ == "__main__":
    create_app().run()
