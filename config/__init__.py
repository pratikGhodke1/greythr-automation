"""Application Configuration"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Flask Application Settings."""

    ENV: str = "production"
    DEBUG: bool = True
    FLASK_APP: str = "app.py"
    URL_PREFIX: str = "/api/v1"
    # SERVER_NAME: str = "localhost:5000"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///prod.sqlite3"

    # Schedular Configuration
    SCHEDULER_API_ENABLED: bool = True
    JSONIFY_PRETTYPRINT_REGULAR: bool = True
