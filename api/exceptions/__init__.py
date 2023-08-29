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


class AutoSignFailedError(Exception):
    """Auto Sign operation failed exception"""

    def __init__(self, error: str = "") -> None:
        self.status_code = 422
        self.message = f"Process Failed! {error}"
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Unauthorized exception"""

    def __init__(self) -> None:
        self.status_code = 401
        self.message = "EE na chalbe!!"
        super().__init__(self.message)
