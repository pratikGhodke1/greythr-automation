"""Employee Schema Structure."""

from werkzeug.security import check_password_hash
from api.model import db


class Employee(db.Model):
    """Employee Model"""

    __tablename__ = "employees"

    eid = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))

    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Return a string representation of User."""
        return f"<Employee: Name={self.name}, EID={self.eid}>"
