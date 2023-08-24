"""Request validation models"""

from pydantic import BaseModel


class EmployeesPostRequest(BaseModel):
    """Employees POST request validation model"""

    name: str
    eid: str = ""
    password: str
