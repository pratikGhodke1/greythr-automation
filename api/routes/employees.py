"""User routes."""

from flask import make_response
from flask_restful import Resource
from flask_pydantic import validate

from api.schema.validation import EmployeesPostRequest
from api.routes.helper import create_blueprint, create_restful_api
from api.service.employee import register_employee, delete_employee
from api.service.greythr_automation import execute_sign_operation


class EmployeesAPI(Resource):
    """API to handle users related operations."""

    def get(self):
        """Simple test endpoint for development. Will be removed later."""
        return "Hello World!"

    @validate()
    def post(self, body: EmployeesPostRequest):
        """Register an employee"""
        print("Received request to create a new employee")
        register_employee(body.model_dump())
        print("Employee added!")
        return make_response({"message": "All Set! ;)"}, 201)


class EmployeeAPI(Resource):
    """API to handle individual employee operations."""

    def delete(self, eid: str):
        """Delete an employee entry."""
        print("Received request to delete employee entry")
        delete_employee(eid.lower())
        print("Employee record deleted!")
        return "", 204


class PunchAPI(Resource):
    """API to sign-in/sign-off."""

    def get(self, eid: str):
        """Auto sign-in/sign-off."""

        print(f"Received request to Auto Sign in {eid=} GreytHR.")
        execute_sign_operation(eid.lower())
        print(f"Auto Signed for {eid=}!")
        return "SUCCESS", 201


employees_blueprint = create_blueprint("employee", __name__)
employees_api = create_restful_api(employees_blueprint)

# Register routes
employees_api.add_resource(EmployeesAPI, "/employee")
employees_api.add_resource(EmployeeAPI, "/employee/<eid>")
employees_api.add_resource(PunchAPI, "/employee/punch/<eid>")
