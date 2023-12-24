import warnings
from functools import wraps
from typing import Callable

from .exceptions import GeckoTerminalParameterWarning

MAX_PAGE = 10
MAX_ADDRESSES = 30
INCLUDE_LIST = ["base_token", "quote_token", "dex", "network", "top_pools"]
TIMEFRAMES = ["day", "hour", "minute"]
DAY_AGGREGATE = [1]
HOUR_AGGREGATE = [1, 4, 12]
MINUTE_AGGREGATE = [1, 5, 15]
OHLCV_LIMIT = 1000
CURRENCY = ["usd", "token"]
TOKEN = ["base", "quote"]


def validate_page(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "page" in kwargs and kwargs["page"] > MAX_PAGE:
            warnings.warn(
                f"Maximum {MAX_PAGE} pages allowed, {kwargs['page']} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return func(*args, **kwargs)

    return wrapper


def validate_addresses(func: Callable):
    @wraps(func)
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
        return func(*args, **kwargs)

    return wrapper


def validate_include(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "include" in kwargs and not set(kwargs["include"]).issubset(INCLUDE_LIST):
            warnings.warn(
                f"Include list can have: {INCLUDE_LIST}",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return func(*args, **kwargs)

    return wrapper


def validate_timeframe(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "timeframe" in kwargs and kwargs["timeframe"] not in TIMEFRAMES:
            warnings.warn(
                f"Timeframe can be: {TIMEFRAMES}",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return func(*args, **kwargs)

    return wrapper


def validate_aggregate(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "aggregate" in kwargs and "timeframe" in kwargs:
            match kwargs["timeframe"]:
                case "day":
                    valid_agg = DAY_AGGREGATE
                case "hour":
                    valid_agg = HOUR_AGGREGATE
                case "minute":
                    valid_agg = MINUTE_AGGREGATE
                case _:
                    valid_agg = []

            if kwargs["aggregate"] not in valid_agg:
                warnings.warn(
                    f"Aggregate can be {valid_agg} when timeframe is {kwargs['timeframe']}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )

        return func(*args, **kwargs)

    return wrapper


def validate_ohlcv_limit(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "ohlcv_limit" in kwargs and kwargs["ohlcv_limit"] > OHLCV_LIMIT:
            warnings.warn(
                f"Maximum {OHLCV_LIMIT} OHLCV allowed, {kwargs['ohlcv_limit']} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return func(*args, **kwargs)

    return wrapper


def validate_currency(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "currency" in kwargs and kwargs["currency"] not in CURRENCY:
            warnings.warn(
                f"Currency can be: {CURRENCY}",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return func(*args, **kwargs)

    return wrapper


def validate_token(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "token" in kwargs and kwargs["token"] not in TOKEN:
            warnings.warn(
                f"Token can be: {TOKEN}",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return func(*args, **kwargs)

    return wrapper
