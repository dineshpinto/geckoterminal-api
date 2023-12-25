import pytest

from geckoterminal_api import (
    GeckoTerminalParameterWarning,
)
from geckoterminal_api.validation import (
    INCLUDE_LIST,
    MAX_ADDRESSES,
    MAX_PAGE,
    OHLCV_LIMIT,
    validate_addresses,
    validate_aggregate,
    validate_currency,
    validate_include,
    validate_ohlcv_limit,
    validate_page,
    validate_timeframe,
    validate_token,
)


@validate_page
@validate_addresses
@validate_include
@validate_timeframe
@validate_aggregate
@validate_ohlcv_limit
@validate_currency
@validate_token
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
        func(include=[*INCLUDE_LIST, "invalid_include"])


def test_timeframe_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(timeframe="invalid_timeframe")


def test_aggregate_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(timeframe="day", aggregate=69)


def test_ohlcv_limit_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(ohlcv_limit=OHLCV_LIMIT + 1)


def test_currency_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(currency="invalid_currency")


def test_token_validation():
    with pytest.warns(GeckoTerminalParameterWarning):
        func(token="invalid_token")
