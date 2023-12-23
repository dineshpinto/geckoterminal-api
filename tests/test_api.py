import pytest

from geckoterminal_api import GeckoTerminalAPI


@pytest.fixture(scope="module")
def api():
    return GeckoTerminalAPI()


def test_networks(api):
    networks = api.networks()
    assert isinstance(networks, dict)
    assert "data" in networks


def test_dexes(api):
    dexes = api.dexes(network="eth")
    assert isinstance(dexes, dict)
    assert "data" in dexes


def test_trending_pools(api):
    trending_pools = api.trending_pools()
    assert isinstance(trending_pools, dict)
    assert "data" in trending_pools


def test_network_trending_pools(api):
    network_trending_pools = api.network_trending_pools(network="eth")
    assert isinstance(network_trending_pools, dict)
    assert "data" in network_trending_pools


def test_network_pool_address(api):
    network_pool_address = api.network_pool_address(
        network="eth", address="0x60594a405d53811d3bc4766596efd80fd545a270"
    )
    assert isinstance(network_pool_address, dict)
    assert "data" in network_pool_address


def test_network_pools_multi_address(api):
    network_pools_multi_address = api.network_pools_multi_address(
        network="eth",
        addresses=[
            "0x60594a405d53811d3bc4766596efd80fd545a270",
            "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
        ],
    )
    assert isinstance(network_pools_multi_address, dict)
    assert "data" in network_pools_multi_address


def test_network_pools(api):
    network_pools = api.network_pools(network="eth")
    assert isinstance(network_pools, dict)
    assert "data" in network_pools


def test_network_dex_pools(api):
    network_dex_pools = api.network_dex_pools(network="eth", dex="sushiswap")
    assert isinstance(network_dex_pools, dict)
    assert "data" in network_dex_pools


def test_network_new_pools(api):
    network_new_pools = api.network_new_pools(network="eth")
    assert isinstance(network_new_pools, dict)
    assert "data" in network_new_pools


def test_new_pools(api):
    new_pools = api.new_pools()
    assert isinstance(new_pools, dict)
    assert "data" in new_pools


def test_search_network_pool(api):
    search_pools = api.search_network_pool(query="ETH", network="eth")
    assert isinstance(search_pools, dict)
    assert "data" in search_pools
