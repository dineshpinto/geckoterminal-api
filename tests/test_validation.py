import pytest

from geckoterminal_api.exceptions import (
    GeckoTerminalParameterWarning,
)
from geckoterminal_api.limits import (
    CURRENCIES,
    DAY_AGGREGATES,
    HOUR_AGGREGATES,
    MAX_ADDRESSES,
    MAX_PAGE,
    MINUTE_AGGREGATES,
    OHLCV_LIMIT,
    POOL_INCLUDES,
    TIMEFRAMES,
    TOKENS,
)
from geckoterminal_api.validation import validate


@validate(
    max_page=MAX_PAGE,
    max_addresses=MAX_ADDRESSES,
    include_list=POOL_INCLUDES,
    timeframes=TIMEFRAMES,
    minute_aggregates=MINUTE_AGGREGATES,
    hour_aggregates=HOUR_AGGREGATES,
    day_aggregates=DAY_AGGREGATES,
    ohlcv_limit=OHLCV_LIMIT,
    tokens=TOKENS,
    currencies=CURRENCIES,
)
def func(**_kwargs):
    """Dummy function for testing parameter validation with decorators."""


def test_page_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(page=MAX_PAGE + 1)


def test_address_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(
            addresses=["0x60594a405d53811d3bc4766596efd80fd545a270"]
            * (MAX_ADDRESSES + 1)
        )


def test_include_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(include=[*POOL_INCLUDES, "invalid_include"])


def test_timeframe_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(timeframe="invalid_timeframe")


def test_aggregate_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(timeframe="day", aggregate=69)


def test_ohlcv_limit_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(limit=OHLCV_LIMIT + 1)


def test_currency_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(currency="invalid_currency")


def test_token_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(token="invalid_token")
