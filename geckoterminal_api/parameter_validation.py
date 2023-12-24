import warnings
from functools import wraps
from typing import Callable

from .exceptions import GeckoTerminalParameterWarning


def validate_page(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "page" in kwargs and kwargs["page"] > 10:
            warnings.warn(
                f"Maximum 10 pages allowed, {kwargs['page']} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    return wrapper


def validate_addresses(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "addresses" in kwargs and len(kwargs["addresses"]) > 30:
            warnings.warn(
                f"Maximum 30 addresses allowed, {len(kwargs['addresses'])} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    return wrapper


def validate_include(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "include" in kwargs and not set(kwargs["include"]).issubset(
                ["base_token", "quote_token", "dex", "network"]
        ):
            warnings.warn(
                "Include list can have: ['base_token', 'quote_token', 'dex', 'network']",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    return wrapper
