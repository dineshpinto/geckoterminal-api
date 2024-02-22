import warnings
from functools import wraps
from typing import Callable

from .exceptions import GeckoTerminalParameterWarning


def validate(**limit_kwargs):
    """Decorator to validate the parameters of the function"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "page" in kwargs and kwargs["page"] > limit_kwargs["max_page"]:
                warnings.warn(
                    f"Maximum {limit_kwargs['max_page']} pages allowed, "
                    f"{kwargs['page']} provided",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            if "include" in kwargs and not set(kwargs["include"]).issubset(
                limit_kwargs["include_list"]
            ):
                warnings.warn(
                    f"Include list can have: {limit_kwargs['include_list']}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            if (
                "addresses" in kwargs
                and (n_addr := len(kwargs["addresses"])) > limit_kwargs["max_addresses"]
            ):
                warnings.warn(
                    f"Maximum {limit_kwargs['max_addresses']} addresses allowed,"
                    f" {n_addr} provided",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            if (
                "timeframe" in kwargs
                and kwargs["timeframe"] not in limit_kwargs["timeframes"]
            ):
                warnings.warn(
                    f"Timeframe can have: {limit_kwargs['timeframes']}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            if "timeframe" in kwargs:
                if (
                    kwargs["timeframe"] == "minute"
                    and kwargs["aggregate"] not in limit_kwargs["minute_aggregates"]
                ):
                    warnings.warn(
                        f"Minute aggregate can have: "
                        f"{limit_kwargs['minute_aggregates']}",
                        GeckoTerminalParameterWarning,
                        stacklevel=2,
                    )
                elif (
                    kwargs["timeframe"] == "hour"
                    and kwargs["aggregate"] not in limit_kwargs["hour_aggregates"]
                ):
                    warnings.warn(
                        f"Hour aggregate can have: {limit_kwargs['hour_aggregates']}",
                        GeckoTerminalParameterWarning,
                        stacklevel=2,
                    )
                elif (
                    kwargs["timeframe"] == "day"
                    and kwargs["aggregate"] not in limit_kwargs["day_aggregates"]
                ):
                    warnings.warn(
                        f"Day aggregate can have: {limit_kwargs['day_aggregates']}",
                        GeckoTerminalParameterWarning,
                        stacklevel=2,
                    )
            if "limit" in kwargs and kwargs["limit"] > limit_kwargs["ohlcv_limit"]:
                warnings.warn(
                    f"Maximum {limit_kwargs['ohlcv_limit']} limit allowed, "
                    f"{kwargs['limit']} provided",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            if (
                "currency" in kwargs
                and kwargs["currency"] not in limit_kwargs["currencies"]
            ):
                warnings.warn(
                    f"Currency can have: {limit_kwargs['currencies']}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            if "token" in kwargs and kwargs["token"] not in limit_kwargs["tokens"]:
                warnings.warn(
                    f"Token can have: {limit_kwargs['tokens']}",
                    GeckoTerminalParameterWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
