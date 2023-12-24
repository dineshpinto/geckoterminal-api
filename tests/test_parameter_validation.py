import pytest

from geckoterminal_api import (
    GeckoTerminalAPI,
    GeckoTerminalAPIError,
    GeckoTerminalParameterWarning,
)
from geckoterminal_api.parameter_validation import INCLUDE_LIST, MAX_ADDRESSES, MAX_PAGE


@pytest.fixture(scope="module")
def api():
    return GeckoTerminalAPI()


def test_page_validation(api):
    with pytest.raises(GeckoTerminalAPIError):  # noqa: SIM117
        with pytest.warns(GeckoTerminalParameterWarning):
            api.network_pools(network="eth", page=MAX_PAGE + 1)


def test_addresses_validation(api):
    with pytest.raises(GeckoTerminalAPIError):  # noqa: SIM117
        with pytest.warns(GeckoTerminalParameterWarning):
            api.network_pools_multi_address(
                network="eth",
                addresses=["0x60594a405d53811d3bc4766596efd80fd545a270"]
                * (MAX_ADDRESSES + 1),
            )


def test_include_validation(api):
    with pytest.warns(GeckoTerminalParameterWarning):
        api.network_pools(
            network="eth",
            include=[*INCLUDE_LIST, "invalid_include"],
        )
