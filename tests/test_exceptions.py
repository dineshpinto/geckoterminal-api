import pytest

from geckoterminal_api import (
    GeckoTerminalAPI,
    GeckoTerminalAPIError,
)


@pytest.fixture(scope="module")
def client():
    return GeckoTerminalAPI()


def test_api_exception(client):
    # raises 404
    with pytest.raises(GeckoTerminalAPIError):
        client.network_new_pools(network="arb")
