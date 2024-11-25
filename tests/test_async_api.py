import pytest

from geckoterminal_api.async_api import AsyncGeckoTerminalAPI


@pytest.fixture(scope="module")
def async_client() -> AsyncGeckoTerminalAPI:
    return AsyncGeckoTerminalAPI()


@pytest.mark.asyncio
async def test_networks(async_client: AsyncGeckoTerminalAPI) -> None:
    networks = await async_client.networks()
    assert isinstance(networks, dict)
    assert "data" in networks
    assert "id" in networks["data"][0]
    assert "type" in networks["data"][0]
    assert "attributes" in networks["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_dexes(async_client: AsyncGeckoTerminalAPI) -> None:
    dexes = await async_client.network_dexes(network="eth")
    assert isinstance(dexes, dict)
    assert "data" in dexes
    assert "id" in dexes["data"][0]
    assert "type" in dexes["data"][0]
    assert "attributes" in dexes["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_trending_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    trending_pools = await async_client.trending_pools()
    assert isinstance(trending_pools, dict)
    assert "data" in trending_pools
    assert "id" in trending_pools["data"][0]
    assert "type" in trending_pools["data"][0]
    assert "attributes" in trending_pools["data"][0]
    assert "base_token_price_usd" in trending_pools["data"][0]["attributes"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_trending_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    network_trending_pools = await async_client.network_trending_pools(network="eth")
    assert isinstance(network_trending_pools, dict)
    assert "data" in network_trending_pools
    assert "id" in network_trending_pools["data"][0]
    assert "type" in network_trending_pools["data"][0]
    assert "attributes" in network_trending_pools["data"][0]
    assert "base_token_price_usd" in network_trending_pools["data"][0]["attributes"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_pool_address(async_client: AsyncGeckoTerminalAPI) -> None:
    network_pool_address = await async_client.network_pool_address(
        network="eth", address="0x60594a405d53811d3bc4766596efd80fd545a270"
    )
    assert isinstance(network_pool_address, dict)
    assert "data" in network_pool_address
    assert "id" in network_pool_address["data"]
    assert "type" in network_pool_address["data"]
    assert "attributes" in network_pool_address["data"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_pools_multi_address(async_client: AsyncGeckoTerminalAPI) -> None:
    network_pools_multi_address = await async_client.network_pools_multi_address(
        network="eth",
        addresses=[
            "0x60594a405d53811d3bc4766596efd80fd545a270",
            "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
        ],
    )
    assert isinstance(network_pools_multi_address, dict)
    assert "data" in network_pools_multi_address
    assert "included" in network_pools_multi_address
    assert "id" in network_pools_multi_address["data"][0]
    assert "type" in network_pools_multi_address["data"][0]
    assert "attributes" in network_pools_multi_address["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    network_pools = await async_client.network_pools(network="eth")
    assert isinstance(network_pools, dict)
    assert "data" in network_pools
    assert "id" in network_pools["data"][0]
    assert "type" in network_pools["data"][0]
    assert "attributes" in network_pools["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_dex_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    network_dex_pools = await async_client.network_dex_pools(
        network="eth", dex="sushiswap"
    )
    assert isinstance(network_dex_pools, dict)
    assert "data" in network_dex_pools
    assert "id" in network_dex_pools["data"][0]
    assert "type" in network_dex_pools["data"][0]
    assert "attributes" in network_dex_pools["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_new_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    network_new_pools = await async_client.network_new_pools(network="eth")
    assert isinstance(network_new_pools, dict)
    assert "data" in network_new_pools
    assert "id" in network_new_pools["data"][0]
    assert "type" in network_new_pools["data"][0]
    assert "attributes" in network_new_pools["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_new_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    new_pools = await async_client.new_pools()
    assert isinstance(new_pools, dict)
    assert "data" in new_pools
    assert "id" in new_pools["data"][0]
    assert "type" in new_pools["data"][0]
    assert "attributes" in new_pools["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_search_network_pool(async_client: AsyncGeckoTerminalAPI) -> None:
    search_pools = await async_client.search_network_pool(query="ETH", network="eth")
    assert isinstance(search_pools, dict)
    assert "data" in search_pools
    assert "id" in search_pools["data"][0]
    assert "type" in search_pools["data"][0]
    assert "attributes" in search_pools["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_addresses_token_price(
    async_client: AsyncGeckoTerminalAPI,
) -> None:
    network_addresses_token_price = await async_client.network_addresses_token_price(
        network="eth",
        addresses=[
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        ],
    )
    assert isinstance(network_addresses_token_price, dict)
    assert "data" in network_addresses_token_price
    assert "id" in network_addresses_token_price["data"]
    assert "type" in network_addresses_token_price["data"]
    assert "attributes" in network_addresses_token_price["data"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_token_pools(async_client: AsyncGeckoTerminalAPI) -> None:
    network_token_pools = await async_client.network_token_pools(
        network="eth", token_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    )
    assert isinstance(network_token_pools, dict)
    assert "data" in network_token_pools
    assert "id" in network_token_pools["data"][0]
    assert "type" in network_token_pools["data"][0]
    assert "attributes" in network_token_pools["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_token(async_client: AsyncGeckoTerminalAPI) -> None:
    network_token = await async_client.network_token(
        network="eth", address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    )
    assert isinstance(network_token, dict)
    assert "data" in network_token
    assert "id" in network_token["data"]
    assert "type" in network_token["data"]
    assert "attributes" in network_token["data"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_tokens_multi_address(
    async_client: AsyncGeckoTerminalAPI,
) -> None:
    network_tokens_multi_address = await async_client.network_tokens_multi_address(
        network="eth",
        addresses=[
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        ],
    )
    assert isinstance(network_tokens_multi_address, dict)
    assert "data" in network_tokens_multi_address
    assert "included" in network_tokens_multi_address
    assert "id" in network_tokens_multi_address["data"][0]
    assert "type" in network_tokens_multi_address["data"][0]
    assert "attributes" in network_tokens_multi_address["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_tokens_address_info(async_client: AsyncGeckoTerminalAPI) -> None:
    network_tokens_address_info = await async_client.network_tokens_address_info(
        network="eth", address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )
    assert isinstance(network_tokens_address_info, dict)
    assert "data" in network_tokens_address_info
    assert "id" in network_tokens_address_info["data"]
    assert "type" in network_tokens_address_info["data"]
    assert "attributes" in network_tokens_address_info["data"]
    await async_client.close()


@pytest.mark.asyncio
async def test_token_info_recently_updated(async_client: AsyncGeckoTerminalAPI) -> None:
    token_info_recently_updated = await async_client.token_info_recently_updated()
    assert isinstance(token_info_recently_updated, dict)
    assert "data" in token_info_recently_updated
    assert "id" in token_info_recently_updated["data"][0]
    assert "type" in token_info_recently_updated["data"][0]
    assert "attributes" in token_info_recently_updated["data"][0]
    assert "description" in token_info_recently_updated["data"][0]["attributes"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_pool_ohlcv(async_client: AsyncGeckoTerminalAPI) -> None:
    network_pool_ohlcv = await async_client.network_pool_ohlcv(
        network="eth",
        pool_address="0x60594a405d53811d3bc4766596efd80fd545a270",
        timeframe="day",
        aggregate=1,
    )
    assert isinstance(network_pool_ohlcv, dict)
    assert "data" in network_pool_ohlcv
    assert "id" in network_pool_ohlcv["data"]
    assert "type" in network_pool_ohlcv["data"]
    assert "attributes" in network_pool_ohlcv["data"]
    assert "ohlcv_list" in network_pool_ohlcv["data"]["attributes"]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_pool_trades(async_client: AsyncGeckoTerminalAPI) -> None:
    network_pool_trades = await async_client.network_pool_trades(
        network="eth", pool_address="0x60594a405d53811d3bc4766596efd80fd545a270"
    )
    assert isinstance(network_pool_trades, dict)
    assert "data" in network_pool_trades
    assert "id" in network_pool_trades["data"][0]
    assert "type" in network_pool_trades["data"][0]
    assert "attributes" in network_pool_trades["data"][0]
    await async_client.close()


@pytest.mark.asyncio
async def test_network_pool_info(async_client: AsyncGeckoTerminalAPI) -> None:
    network_pool_info = await async_client.network_pool_info(
        network="eth", pool_address="0x60594a405d53811d3bc4766596efd80fd545a270"
    )
    assert isinstance(network_pool_info, dict)
    assert isinstance(network_pool_info["data"], list)
    assert "data" in network_pool_info
    assert "id" in network_pool_info["data"][0]
    assert "type" in network_pool_info["data"][0]
    assert "attributes" in network_pool_info["data"][0]
    await async_client.close()
