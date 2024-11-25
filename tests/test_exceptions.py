import pytest

from geckoterminal_api.api import GeckoTerminalAPI
from geckoterminal_api.exceptions import GeckoTerminalAPIError


@pytest.fixture(scope="module")
def client() -> GeckoTerminalAPI:
    return GeckoTerminalAPI()


def test_api_exception(client) -> None:
    # raises 404
    with pytest.raises(GeckoTerminalAPIError):
        client.network_new_pools(network="arb")
