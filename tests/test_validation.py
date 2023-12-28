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
from geckoterminal_api.validation import (
    validate_addresses,
    validate_aggregate,
    validate_currency,
    validate_include,
    validate_limit,
    validate_page,
    validate_timeframe,
    validate_token,
)


@validate_page(0, MAX_PAGE)
@validate_addresses(MAX_ADDRESSES)
@validate_include(POOL_INCLUDES)
@validate_timeframe(TIMEFRAMES)
@validate_aggregate(MINUTE_AGGREGATES, HOUR_AGGREGATES, DAY_AGGREGATES)
@validate_limit(OHLCV_LIMIT)
@validate_token(TOKENS)
@validate_currency(CURRENCIES)
def func(**_kwargs):
    """Dummy function for testing parameter validation with decorators"""


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
