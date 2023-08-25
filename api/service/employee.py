"""User Service."""

from cryptography.fernet import Fernet

from api.exceptions import EmployeeAlreadyExists, EmployeeDoesNotExists
from api.model import db
from api.model.employee import Employee

fernet = Fernet(b'4VnnKxIio0WQnBkIgL8t0FJolYfwb-zl6_8GrqUaNhA=')


def encrypt(text: str) -> bytes:
    """Encrypt a string.

    Args:
        text (str): Text to be encrypted

    Returns:
        bytes: Encrypted string
    """
    return fernet.encrypt(text.encode())


def decrypt(encrypted_string: bytes) -> str:
    """Decrypt bytes string.

    Args:
        encrypted_string (bytes): Encrypted string

    Returns:
        str: Decrypted string
    """
    return fernet.decrypt(encrypted_string).decode()


def register_employee(employee_info: dict) -> dict:
    """Register an employee in the database.

    Args:
        employee_info (dict): New user information

    Raises:
        UserAlreadyExists: User already exists error

    Returns:
        dict: Added employee information
    """
    employee_info["eid"] = employee_info["eid"].lower()
    employee_info["password"] = encrypt(employee_info["password"])
    eid = employee_info["eid"]

    if Employee.query.filter(Employee.eid == eid).first():
        raise EmployeeAlreadyExists()

    new_user = Employee(**employee_info)
    db.session.add(new_user)
    db.session.commit()


def delete_employee(eid: str):
    """Delete an employee ID.

    Args:
        eid (str): Employee ID
    """
    employee = Employee.query.filter(Employee.eid == eid).first()

    if not employee:
        raise EmployeeDoesNotExists()

    db.session.delete(employee)
    db.session.commit()
