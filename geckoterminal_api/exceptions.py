class GeckoTerminalAPIError(Exception):
    """Generic exception for API communication"""

    def __init__(self, status: int, err: str):
        self.status = status
        self.err = err

    def __str__(self):
        return f"(status={self.status}) {self.err}"


class GeckoTerminalParameterWarning(Warning):
    """Warning for (potentially) invalid parameters"""
