import json
from typing import Optional

import requests

from .exceptions import GeckoTerminalAPIError
from .parameter_validation import (
    validate_addresses,
    validate_aggregate,
    validate_currency,
    validate_include,
    validate_ohlcv_limit,
    validate_page,
    validate_timeframe,
    validate_token,
)


class GeckoTerminalAPI:
    """RESTful Python client for GeckoTerminal API."""

    def __init__(self, api_version: Optional[str] = None):
        """
        Args:
            api_version: GeckoTerminal API version, if None latest will be used
        """
        self.base_url = "https://api.geckoterminal.com/api/v2"
        self.accept_header = (
            f"application/json;version={api_version}"
            if api_version
            else "application/json"
        )
        self._session = requests.Session()

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        headers = {"accept": self.accept_header}
        url = self.base_url + endpoint
        response = self._session.request(
            method="GET", url=url, params=params, headers=headers, timeout=30
        )

        match response.status_code:
            case 200:
                return response.json()
            case 404:
                errors = ",".join(
                    r["title"] for r in json.loads(response.text)["errors"]
                )
                raise GeckoTerminalAPIError(
                    status=response.status_code,
                    err=errors,
                )
            case 429:
                raise GeckoTerminalAPIError(
                    status=response.status_code,
                    err=f"Rate Limited (limit = {json.loads(response.text)['limit']})",
                )
            case _:
                raise GeckoTerminalAPIError(
                    status=response.status_code,
                    err=response.text,
                )

    def networks(self, page: int = 1) -> dict:
        """Get list of supported networks

        Args:
            page: Page through results (default 1)
        """
        return self._get(endpoint="/networks", params={"page": page})

    def network_dexes(self, network: str, page: int = 1) -> dict:
        """Get list of supported dexes on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            page: Page through results (default 1)
        """
        return self._get(endpoint=f"/networks/{network}/dexes", params={"page": page})

    @validate_include
    @validate_page
    def trending_pools(self, include: Optional[list] = None, page: int = 1) -> dict:
        """Get trending pools across all networks

        Args:
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex, network (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex", "network"]
        return self._get(
            endpoint="/networks/trending_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    @validate_page
    def network_trending_pools(
        self, network: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get trending pools on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/trending_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    def network_pool_address(
        self,
        network: str,
        address: str,
        include: Optional[list] = None,
    ) -> dict:
        """Get specific pool on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            address: Address of pool e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/pools/{address}",
            params={
                "include": ",".join(include),
            },
        )

    @validate_addresses
    @validate_include
    def network_pools_multi_address(
        self, network: str, addresses: list[str], include: Optional[list] = None
    ) -> dict:
        """Get multiple pools on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            addresses: List of pool addresses
                e.g. ["0x60594a405d53811d3bc4766596efd80fd545a270",
                "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"]
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/pools/multi/{','.join(addresses)}",
            params={
                "include": ",".join(include),
            },
        )

    @validate_include
    @validate_page
    def network_pools(
        self, network: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get top pools on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    @validate_page
    def network_dex_pools(
        self, network: str, dex: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get top pools on a network's dex

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            dex: Dex id from `dexes()` e.g. sushiswap, raydium, uniswap_v3
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/dexes/{dex}/pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    @validate_page
    def network_new_pools(
        self, network: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get new pools on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]

        return self._get(
            endpoint=f"/networks/{network}/new_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    @validate_page
    def new_pools(self, include: Optional[list] = None, page: int = 1) -> dict:
        """Get new pools across all networks

        Args:
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex, network (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex", "network"]
        return self._get(
            endpoint="/networks/new_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    @validate_page
    def search_network_pool(
        self,
        query: str,
        network: Optional[str] = None,
        include: Optional[list] = None,
        page: int = 1,
    ) -> dict:
        """Search for a pool on a network

        Args:
            query: Search query: can be pool address, token address, or token symbol
                e.g. "ETH"
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint="/search/pools",
            params={
                "query": query,
                "network": network,
                "include": ",".join(include),
                "page": page,
            },
        )

    @validate_addresses
    def network_addresses_token_price(self, network: str, addresses: list[str]) -> dict:
        """Get current USD prices of multiple tokens on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            addresses: List of token addresses
                e.g. ["0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"]
        """
        return self._get(
            endpoint=f"/simple/networks/{network}/token_price/{','.join(addresses)}",
        )

    @validate_include
    @validate_page
    def network_token_pools(
        self,
        network: str,
        token_address: str,
        include: Optional[list] = None,
        page: int = 1,
    ) -> dict:
        """Get top pools for a token on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            token_address: Address of token e.g. 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/tokens/{token_address}/pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate_include
    def network_token(
        self, network: str, address: str, include: Optional[list] = None
    ) -> dict:
        """Get specific token on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            address: Address of token e.g. 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
            include: List of related resources to include in response. Available
                resources are: top_pools (default top_pools)
        """
        if include is None:
            include = ["top_pools"]
        return self._get(
            endpoint=f"/networks/{network}/tokens/{address}",
            params={"include": ",".join(include)},
        )

    @validate_addresses
    @validate_include
    def network_tokens_multi_address(
        self, network: str, addresses: list[str], include: Optional[list] = None
    ) -> dict:
        """Get multiple tokens on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            addresses: List of token addresses
                e.g. ["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"]
            include: List of related resources to include in response. Available
                resources are: top_pools (default top_pools)
        """
        if include is None:
            include = ["top_pools"]
        return self._get(
            endpoint=f"/networks/{network}/tokens/multi/{','.join(addresses)}",
            params={"include": ",".join(include)},
        )

    def network_tokens_address_info(self, network: str, address: str) -> dict:
        """Get token address info on a network

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            address: Address of token e.g. 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
        """
        return self._get(
            endpoint=f"/networks/{network}/tokens/{address}/info",
        )

    def token_info_recently_updated(self, include: Optional[list] = None):
        """Get most recently updated 100 tokens info from all networks

        Args:
            include: List of related resources to include in response. Available
                resources are: network (default network)
        """
        if include is None:
            include = ["network"]
        return self._get(
            endpoint="/tokens/info_recently_updated",
            params={"include": ",".join(include)},
        )

    @validate_timeframe
    @validate_aggregate
    @validate_ohlcv_limit
    @validate_currency
    @validate_token
    def network_pool_ohlcv(
        self,
        network: str,
        pool_address: str,
        timeframe: str,
        aggregate: Optional[int] = 1,
        before_timestamp: Optional[int] = None,
        limit: Optional[int] = 100,
        currency: Optional[str] = "usd",
        token: Optional[str] = "base",
    ) -> dict:
        """Get OHLCV data of a pool

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            pool_address: Address of pool
                e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
            timeframe: Timeframe of OHLCV data e.g. day, hour, minute
            aggregate: Aggregate of OHLCV data e.g. day (1), hour ([1, 4, 12])
                and minute ([1, 5, 15]) (default 1)
            before_timestamp: Timestamp to get OHLCV data before e.g. 1679414400
            limit: Limit of OHLCV data (default 100, max 1000)
            currency: Currency of OHLCV data e.g. usd, token (default usd)
            token: Token of OHLCV data e.g. base, quote (default base)
        """
        params = {
            "aggregate": aggregate,
            "before_timestamp": before_timestamp,
            "limit": limit,
            "currency": currency,
            "token": token,
        }
        return self._get(
            endpoint=f"/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}",
            params=params,
        )

    def network_pool_trades(
        self,
        network: str,
        pool_address: str,
        trade_volume_in_usd_greater_than: Optional[int] = None,
    ) -> dict:
        """Get trades of a pool

        Args:
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            pool_address: Address of pool
                e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
            trade_volume_in_usd_greater_than: Trade volume in USD greater than
                e.g. 100000 (default 0)
        """
        return self._get(
            endpoint=f"/networks/{network}/pools/{pool_address}/trades",
            params={
                "trade_volume_in_usd_greater_than": trade_volume_in_usd_greater_than,
            },
        )
