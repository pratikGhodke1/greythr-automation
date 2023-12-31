"""User routes."""

from flask import make_response, request
from flask_restful import Resource
from flask_pydantic import validate

from api.exceptions import AutoSignFailedError
from api.modules.logger import init_logger
from api.schema.validation import EmployeesPostRequest
from api.routes.helper import create_blueprint, create_restful_api
from api.service.auth import is_allowed
from api.service.employee import register_employee, delete_employee
from api.service.greythr_automation import execute_sign_operation

logger = init_logger(__name__, "EMPLOYEE_SERVICE", request)


class EmployeesAPI(Resource):
    """API to handle users related operations."""

    def get(self):
        """Simple test endpoint for development. Will be removed later."""
        return "Hello World! 👋 Send your 'name', 'eid' and 'password' to me. I will handle it all. If you are on leave, delete your entry from here by hitting DELETE api/v1/employee/s123 👈 'your eid here'. Use 'BASIC AUTH' with your eid and greytHR password as username and password respectively 🤗"

    @validate()
    def post(self, body: EmployeesPostRequest):
        """Register an employee"""
        logger.info("Received request to create a new employee")
        register_employee(body.model_dump())
        logger.info("Employee added!")
        return make_response(
            {
                "message": "All Set! 😉 Do not disclose existence of this application.🤐",
                "note": "If you are on leave, delete your entry from here by hitting DELETE api/v1/employee/s123 👈 'your eid here'. Use 'BASIC AUTH' with your eid and greytHR password as username and password respectively 🤗",
            },
            201,
        )


class EmployeeAPI(Resource):
    """API to handle individual employee operations."""

    @is_allowed
    def delete(self, eid: str):
        """Delete an employee entry."""
        logger.info(f"Received request to delete employee {eid=} entry")
        delete_employee(eid.lower())
        logger.info("Employee record deleted!")
        return "", 204


class PunchAPI(Resource):
    """API to sign-in/sign-off."""

    def get(self, eid: str):
        """Auto sign-in/sign-off."""

        logger.info(f"Received request to Auto Sign in {eid=} GreytHR.")

        try:
            execute_sign_operation(eid.lower())
        except Exception as err:
            logger.exception(str(err))
            raise AutoSignFailedError(str(err)) from err

        logger.info(f"Auto Signed for {eid=}!")
        return "😈", 201


employees_blueprint = create_blueprint("employee", __name__)
employees_api = create_restful_api(employees_blueprint)

# Register routes
employees_api.add_resource(EmployeesAPI, "/employee")
employees_api.add_resource(EmployeeAPI, "/employee/<eid>")
employees_api.add_resource(PunchAPI, "/employee/punch/<eid>")
