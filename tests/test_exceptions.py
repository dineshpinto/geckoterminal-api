import pytest

from geckoterminal_api import (
    GeckoTerminalAPI,
    GeckoTerminalAPIError,
)


@pytest.fixture(scope="module")
def api():
    return GeckoTerminalAPI()


def test_api_exception(api):
    # raises 404
    with pytest.raises(GeckoTerminalAPIError):
        api.network_new_pools(network="arb")
