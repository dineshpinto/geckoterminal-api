from typing import override


class GeckoTerminalAPIError(Exception):
    """Generic exception for API communication"""

    def __init__(self, status: int, err: str) -> None:
        self.status = status
        self.err = err

    @override
    def __str__(self) -> str:
        return f"(status={self.status}) {self.err}"


class GeckoTerminalParameterWarning(Warning):
    """Warning for (potentially) invalid parameters"""
