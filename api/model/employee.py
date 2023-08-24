"""Employee Schema Structure."""

from api.model import db


class Employee(db.Model):
    """Employee Model"""

    __tablename__ = "employees"

    eid = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __repr__(self) -> str:
        """Return a string representation of User."""
        return f"<Employee: Name={self.name}, EID={self.eid}>"
