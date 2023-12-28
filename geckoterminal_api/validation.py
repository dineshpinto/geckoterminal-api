import warnings
from functools import wraps
from typing import Callable

from .exceptions import GeckoTerminalParameterWarning


def validate_page(max_page: int):
    """Validate page parameter sent to API"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "page" in kwargs and kwargs["page"] > max_page:
                warnings.warn(
                    f"Maximum {max_page} pages allowed, {kwargs['page']} provided",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_include(include_list: list):
    """Validate include parameter sent to API"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "include" in kwargs and not set(kwargs["include"]).issubset(
                include_list
            ):
                warnings.warn(
                    f"Include list can have: {include_list}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_addresses(max_addresses: int):
    """Validate addresses parameter sent to API"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (
                "addresses" in kwargs
                and (n_addr := len(kwargs["addresses"])) > max_addresses
            ):
                warnings.warn(
                    f"Maximum {max_addresses} addresses allowed, {n_addr} provided",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_timeframe(timeframes: list):
    """Validate timeframe parameter sent to API"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "timeframe" in kwargs and kwargs["timeframe"] not in timeframes:
                warnings.warn(
                    f"Timeframe can have: {timeframes}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_aggregate(
    minute_aggregate: list,
    hour_aggregate: list,
    day_aggregate: list,
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "timeframe" in kwargs:
                if (
                    kwargs["timeframe"] == "minute"
                    and kwargs["aggregate"] not in minute_aggregate
                ):
                    warnings.warn(
                        f"Minute aggregate can have: {minute_aggregate}",
                        GeckoTerminalParameterWarning,
                        stacklevel=2,
                    )
                elif (
                    kwargs["timeframe"] == "hour"
                    and kwargs["aggregate"] not in hour_aggregate
                ):
                    warnings.warn(
                        f"Hour aggregate can have: {hour_aggregate}",
                        GeckoTerminalParameterWarning,
                        stacklevel=2,
                    )
                elif (
                    kwargs["timeframe"] == "day"
                    and kwargs["aggregate"] not in day_aggregate
                ):
                    warnings.warn(
                        f"Day aggregate can have: {day_aggregate}",
                        GeckoTerminalParameterWarning,
                        stacklevel=2,
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_limit(ohlcv_limit: int):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "limit" in kwargs and kwargs["limit"] > ohlcv_limit:
                warnings.warn(
                    f"Maximum {ohlcv_limit} limit allowed, {kwargs['limit']} provided",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_currency(currencies: list):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "currency" in kwargs and kwargs["currency"] not in currencies:
                warnings.warn(
                    f"Currency can have: {currencies}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_token(tokens: list):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "token" in kwargs and kwargs["token"] not in tokens:
                warnings.warn(
                    f"Token can have: {tokens}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
