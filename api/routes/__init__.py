"""Register routes to the flask application."""

from flask import Flask
from api.routes.employees import employees_blueprint
from api.routes.monitor import monitor_blueprint


def init_routes(app: Flask) -> None:
    """Initialize and assign the routes to flask app

    Args:
        app (Flask): Flask application
    """
    app.register_blueprint(employees_blueprint)
    app.register_blueprint(monitor_blueprint)
