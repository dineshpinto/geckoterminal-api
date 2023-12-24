import warnings
from functools import wraps
from typing import Callable

from .exceptions import GeckoTerminalParameterWarning

MAX_PAGE = 10
MAX_ADDRESSES = 30
INCLUDE_LIST = ["base_token", "quote_token", "dex", "network"]


def validate_page(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(kwargs)
        if "page" in kwargs and kwargs["page"] > MAX_PAGE:
            warnings.warn(
                f"Maximum {MAX_PAGE} pages allowed, {kwargs['page']} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    return wrapper


def validate_addresses(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if (
            "addresses" in kwargs
            and (n_addr := len(kwargs["addresses"])) > MAX_ADDRESSES
        ):
            warnings.warn(
                f"Maximum {MAX_ADDRESSES} addresses allowed, {n_addr} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    return wrapper


def validate_include(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "include" in kwargs and not set(kwargs["include"]).issubset(INCLUDE_LIST):
            warnings.warn(
                f"Include list can have: {INCLUDE_LIST}",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    return wrapper
