"""Error Handler Service"""

from flask import Flask
from api.exceptions import EmployeeAlreadyExists, EmployeeDoesNotExists


def _error_response(error: Exception) -> tuple[dict, int]:
    """Error response generator callback

    Args:
        error (Exception): Raised error exception

    Returns:
        tuple[dict, int]: Flask error response and status code
    """
    print("HERE")
    try:
        status_code = error.status_code
    except AttributeError:
        status_code = 500
    print(status_code)
    error_message = ("[INTERNAL ERROR] " if status_code == 500 else "") + str(error)
    print(error_message)

    return (
        {
            "status": "FAILED",
            "message": error_message,
        },
        status_code,
    )


def register_error_handlers(app: Flask):
    """register error handlers to flask application"""
    print("REGISTERING")
    app.register_error_handler(EmployeeAlreadyExists, _error_response)
    app.register_error_handler(EmployeeDoesNotExists, _error_response)
    print("REGISTERED")
