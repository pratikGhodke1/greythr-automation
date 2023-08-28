"""Error Handler Service"""

from flask import Flask
from api.exceptions import (
    EmployeeAlreadyExists,
    EmployeeDoesNotExists,
    AutoSignFailedError,
)


def _error_response(error: Exception) -> tuple[dict, int]:
    """Error response generator callback

    Args:
        error (Exception): Raised error exception

    Returns:
        tuple[dict, int]: Flask error response and status code
    """
    try:
        status_code = error.status_code
    except AttributeError:
        status_code = 500

    error_message = ("[INTERNAL ERROR] " if status_code == 500 else "") + str(error)

    return (
        {
            "status": "FAILED",
            "message": error_message,
        },
        status_code,
    )


def register_error_handlers(app: Flask):
    """register error handlers to flask application"""
    app.register_error_handler(EmployeeAlreadyExists, _error_response)
    app.register_error_handler(EmployeeDoesNotExists, _error_response)
    app.register_error_handler(AutoSignFailedError, _error_response)
