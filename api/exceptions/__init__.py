"""Application Custom Exceptions"""


class EmployeeAlreadyExists(Exception):
    """Employee already exists exception"""

    def __init__(self) -> None:
        self.status_code = 400
        self.message = "Asli ID se aao!"
        super().__init__(self.message)


class EmployeeDoesNotExists(Exception):
    """Employee does not exists exception"""

    def __init__(self) -> None:
        self.status_code = 404
        self.message = "YOU! Does not exist yet!"
        super().__init__(self.message)
