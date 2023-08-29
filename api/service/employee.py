"""User Service."""

from os import environ
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash

from api.exceptions import EmployeeAlreadyExists
from api.model import db
from api.model.employee import Employee
from api.modules.logger import init_logger

logger = init_logger(__name__, "EMPLOYEE_SERVICE_HELPER")
fernet = Fernet(bytes(environ["FERNET_KEY"], encoding="utf-8"))


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
    employee_info["password_hash"] = generate_password_hash(employee_info["password"])
    employee_info["password"] = encrypt(employee_info["password"])
    eid = employee_info["eid"]

    if Employee.query.filter(Employee.eid == eid).first():
        logger.error(f"Employee {eid=} Already Exists!")
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
    db.session.delete(employee)
    db.session.commit()
