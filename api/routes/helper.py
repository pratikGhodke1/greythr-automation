"""Helper functions for defining routes."""

from flask import Blueprint
from flask_restful import Api

from config import Settings


def create_blueprint(blueprint_name: str, import_name: str) -> Blueprint:
    """Create a blueprint for a route.

    Args:
        name (str): Blueprint Name
        import_name (str): Routes file name

    Returns:
        Blueprint: Flask blueprint for the route
    """
    return Blueprint(
        name=blueprint_name, import_name=import_name, url_prefix=Settings().URL_PREFIX
    )


def create_restful_api(blueprint: Blueprint) -> Api:
    """Create a restful API for flask blueprint.

    Args:
        blueprint (Blueprint): Flask blueprint

    Returns:
        Api: Restful API for given blueprint
    """
    return Api(blueprint)
