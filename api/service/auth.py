"""Auth service."""

from functools import wraps
from flask import request
from api.exceptions import EmployeeDoesNotExists, UnauthorizedError
from api.model.employee import Employee
from api.modules.logger import init_logger

logger = init_logger(__name__, "AUTH_SERVICE_HELPER")


def is_allowed(func):
    """Checks if an user is allowed to do this operation."""
    @wraps(func)
    def wrapped(*args, **kwargs):
        eid = request.view_args["eid"]
        employee = Employee.query.filter(Employee.eid == eid).first()

        if not employee:
            logger.error(f"Employee {eid=} Does Not Exists!")
            raise EmployeeDoesNotExists()

        valid_password = employee.verify_password(request.authorization.password)

        if valid_password and eid == request.authorization.username:
            return func(*args, **kwargs)

        raise UnauthorizedError()

    return wrapped
