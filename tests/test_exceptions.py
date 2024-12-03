import pytest

from geckoterminal_api.api import GeckoTerminalAPI
from geckoterminal_api.async_api import AsyncGeckoTerminalAPI
from geckoterminal_api.exceptions import GeckoTerminalAPIError


@pytest.fixture(scope="module")
def client() -> GeckoTerminalAPI:
    return GeckoTerminalAPI()


@pytest.fixture(scope="module")
def async_client() -> AsyncGeckoTerminalAPI:
    return AsyncGeckoTerminalAPI()


def test_api_exception(client) -> None:
    # raises 404
    with pytest.raises(GeckoTerminalAPIError):
        client.network_new_pools(network="arb")


@pytest.mark.asyncio
async def test_async_api_exception(async_client) -> None:
    # raises 404
    with pytest.raises(GeckoTerminalAPIError):
        await async_client.network_new_pools(network="arb")
