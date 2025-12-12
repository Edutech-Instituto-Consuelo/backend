from typing import Any

class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        data: Any = None,
        status_code: int = 400,
    ):
        super().__init__(message)
        self.message = message
        self.data = data
        self.status_code = status_code
