import json
from datetime import datetime

import aiohttp

from .exceptions import GeckoTerminalAPIError
from .limits import (
    CURRENCIES,
    DAY_AGGREGATES,
    HOUR_AGGREGATES,
    MAX_ADDRESSES,
    MAX_PAGE,
    MINUTE_AGGREGATES,
    NETWORK_POOL_INCLUDES,
    OHLCV_LIMIT,
    POOL_INCLUDES,
    TIMEFRAMES,
    TOKEN_INCLUDES,
    TOKEN_INFO_INCLUDES,
    TOKENS,
)
from .validation import validate


class AsyncGeckoTerminalAPI:
    """Asynchronous RESTful Python client for GeckoTerminal API."""

    def __init__(self, api_version: str | None = None, proxy: str | None = None):
        """
        Args:
        ----
            api_version: GeckoTerminal API version, if None latest will be used
            proxy: Proxy to use for the requests
        """
        self.base_url = "https://api.geckoterminal.com/api/v2"
        self.accept_header = (
            f"application/json;version={api_version}"
            if api_version
            else "application/json"
        )
        self.proxy = proxy
        self._session = None

    async def close(self) -> None:
        await self._session.close()
        self._session = None

    async def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """Asynchronous method to send a GET request to the specified endpoint.

        Args:
        ----
            endpoint (str): The API endpoint to send the request to.
            params (Optional[dict], optional): A dictionary of query parameters to
                include in the request. Defaults to None.

        Returns:
        -------
            dict: The JSON response from the API as a dictionary.

        Raises:
        ------
            GeckoTerminalAPIError: If the API response status code is not 200, it raises
                an exception with the status code and error message.
        """
        if self._session is None:
            self._session = aiohttp.ClientSession(raise_for_status=True)
        get_params = {
            "url": self.base_url + endpoint,
            "params": params,
            "headers": {"accept": self.accept_header},
            "proxy": self.proxy,
        }
        async with self._session.get(**get_params) as response:
            response.raise_for_status()
            match response.status:
                case 200:
                    return await response.json()
                case 404:
                    errors = ",".join(
                        r["title"] for r in json.loads(await response.text())["errors"]
                    )
                    raise GeckoTerminalAPIError(
                        status=response.status,
                        err=errors,
                    )
                case 429:
                    rate_limit = json.loads(await response.text())["limit"]
                    raise GeckoTerminalAPIError(
                        status=response.status,
                        err=f"Rate Limited (limit = {rate_limit})",
                    )
                case _:
                    raise GeckoTerminalAPIError(
                        status=response.status, err=await response.text()
                    )

    async def networks(self, page: int = 1) -> dict:
        """Get list of supported networks

        Args:
        ----
            page: Page through results (default 1)
        """
        return await self._get(endpoint="/networks", params={"page": page})

    async def network_dexes(self, network: str, page: int = 1) -> dict:
        """Get list of supported dexes on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            page: Page through results (default 1)
        """
        return await self._get(
            endpoint=f"/networks/{network}/dexes", params={"page": page}
        )

    @validate(max_page=MAX_PAGE, include_list=POOL_INCLUDES)
    async def trending_pools(self, include: list | None = None, page: int = 1) -> dict:
        """Get trending pools across all networks

        Args:
        ----
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex, network (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = POOL_INCLUDES
        return await self._get(
            endpoint="/networks/trending_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(max_page=MAX_PAGE, include_list=NETWORK_POOL_INCLUDES)
    async def network_trending_pools(
        self, network: str, include: list | None = None, page: int = 1
    ) -> dict:
        """Get trending pools on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/trending_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(include_list=NETWORK_POOL_INCLUDES)
    async def network_pool_address(
        self,
        network: str,
        address: str,
        include: list | None = None,
    ) -> dict:
        """Get specific pool on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            address: Address of pool e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/pools/{address}",
            params={
                "include": ",".join(include),
            },
        )

    @validate(max_addresses=MAX_ADDRESSES, include_list=NETWORK_POOL_INCLUDES)
    async def network_pools_multi_address(
        self, network: str, addresses: list[str], include: list | None = None
    ) -> dict:
        """Get multiple pools on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            addresses: List of pool addresses
                e.g. ["0x60594a405d53811d3bc4766596efd80fd545a270",
                "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"]
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/pools/multi/{','.join(addresses)}",
            params={
                "include": ",".join(include),
            },
        )

    @validate(max_page=MAX_PAGE, include_list=NETWORK_POOL_INCLUDES)
    async def network_pools(
        self, network: str, include: list | None = None, page: int = 1
    ) -> dict:
        """Get top pools on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(max_page=MAX_PAGE, include_list=NETWORK_POOL_INCLUDES)
    async def network_dex_pools(
        self, network: str, dex: str, include: list | None = None, page: int = 1
    ) -> dict:
        """Get top pools on a network's dex

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            dex: Dex id from `dexes()` e.g. sushiswap, raydium, uniswap_v3
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/dexes/{dex}/pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(max_page=MAX_PAGE, include_list=NETWORK_POOL_INCLUDES)
    async def network_new_pools(
        self, network: str, include: list | None = None, page: int = 1
    ) -> dict:
        """Get new pools on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES

        return await self._get(
            endpoint=f"/networks/{network}/new_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(max_page=MAX_PAGE, include_list=POOL_INCLUDES)
    async def new_pools(self, include: list | None = None, page: int = 1) -> dict:
        """Get new pools across all networks

        Args:
        ----
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex, network (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = POOL_INCLUDES
        return await self._get(
            endpoint="/networks/new_pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(max_page=MAX_PAGE, include_list=NETWORK_POOL_INCLUDES)
    async def search_network_pool(
        self,
        query: str,
        network: str | None = None,
        include: list | None = None,
        page: int = 1,
    ) -> dict:
        """Search for a pool on a network

        Args:
        ----
            query: Search query: can be pool address, token address, or token symbol
                e.g. "ETH"
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint="/search/pools",
            params={
                "query": query,
                "network": network,
                "include": ",".join(include),
                "page": page,
            },
        )

    @validate(max_addresses=MAX_ADDRESSES)
    async def network_addresses_token_price(
        self, network: str, addresses: list[str]
    ) -> dict:
        """Get current USD prices of multiple tokens on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            addresses: List of token addresses
                e.g. ["0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"]
        """
        return await self._get(
            endpoint=f"/simple/networks/{network}/token_price/{','.join(addresses)}",
        )

    @validate(max_page=MAX_PAGE, include_list=NETWORK_POOL_INCLUDES)
    async def network_token_pools(
        self,
        network: str,
        token_address: str,
        include: list | None = None,
        page: int = 1,
    ) -> dict:
        """Get top pools for a token on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            token_address: Address of token
                e.g. 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
            page: Page through results (default 1)
        """
        if include is None:
            include = NETWORK_POOL_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/tokens/{token_address}/pools",
            params={"include": ",".join(include), "page": page},
        )

    @validate(include_list=TOKEN_INCLUDES)
    async def network_token(
        self, network: str, address: str, include: list | None = None
    ) -> dict:
        """Get specific token on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            address: Address of token e.g. 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
            include: List of related resources to include in response. Available
                resources are: top_pools (default top_pools)
        """
        if include is None:
            include = TOKEN_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/tokens/{address}",
            params={"include": ",".join(include)},
        )

    @validate(max_addresses=MAX_ADDRESSES, include_list=TOKEN_INCLUDES)
    async def network_tokens_multi_address(
        self, network: str, addresses: list[str], include: list | None = None
    ) -> dict:
        """Get multiple tokens on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            addresses: List of token addresses
                e.g. ["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"]
            include: List of related resources to include in response. Available
                resources are: top_pools (default top_pools)
        """
        if include is None:
            include = TOKEN_INCLUDES
        return await self._get(
            endpoint=f"/networks/{network}/tokens/multi/{','.join(addresses)}",
            params={"include": ",".join(include)},
        )

    async def network_tokens_address_info(self, network: str, address: str) -> dict:
        """Get token address info on a network

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            address: Address of token e.g. 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
        """
        return await self._get(
            endpoint=f"/networks/{network}/tokens/{address}/info",
        )

    async def network_pools_info(self, network: str, pool_address: str) -> dict:
       """Get pool tokens info on a network

       Args:
       ----
           network: Network id from `networks()` e.g. eth, solana, arbitrum
           pool_address: Address of pool 
                e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
       """
       return await self._get(
           endpoint=f"/networks/{network}/pools/{pool_address}/info"
       )

    @validate(max_addresses=MAX_ADDRESSES, include_list=TOKEN_INFO_INCLUDES)
    async def token_info_recently_updated(self, include: list | None = None) -> dict:
        """Get most recently updated 100 tokens info from all networks

        Args:
        ----
            include: List of related resources to include in response. Available
                resources are: network (default network)
        """
        if include is None:
            include = TOKEN_INFO_INCLUDES
        return await self._get(
            endpoint="/tokens/info_recently_updated",
            params={"include": ",".join(include)},
        )

    @validate(
        timeframes=TIMEFRAMES,
        minute_aggregates=MINUTE_AGGREGATES,
        hour_aggregates=HOUR_AGGREGATES,
        day_aggregates=DAY_AGGREGATES,
        ohlcv_limit=OHLCV_LIMIT,
        currencies=CURRENCIES,
        tokens=TOKENS,
    )
    async def network_pool_ohlcv(
        self,
        network: str,
        pool_address: str,
        timeframe: str,
        aggregate: int | None = 1,
        before_timestamp: int | None = None,
        limit: int | None = 100,
        currency: str | None = "usd",
        token: str | None = "base",
    ) -> dict:
        """Get OHLCV data of a pool

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            pool_address: Address of pool
                e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
            timeframe: Timeframe of OHLCV data e.g. day, hour, minute
            aggregate: Aggregate of OHLCV data e.g. day (1), hour ([1, 4, 12])
                and minute ([1, 5, 15]) (default 1)
            before_timestamp: Timestamp to get OHLCV data before (seconds since epoch)
                e.g. 1679414400
            limit: Limit of OHLCV data (default 100, max 1000)
            currency: Currency of OHLCV data e.g. usd, token (default usd)
            token: Token of OHLCV data e.g. base, quote (default base)
        """
        params = {
            "aggregate": aggregate,
            "before_timestamp": before_timestamp
            if before_timestamp
            else int(datetime.now().timestamp()),
            "limit": limit,
            "currency": currency,
            "token": token,
        }
        return await self._get(
            endpoint=f"/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}",
            params=params,
        )

    async def network_pool_trades(
        self,
        network: str,
        pool_address: str,
        trade_volume_in_usd_greater_than: int | None = 0,
    ) -> dict:
        """Get trades of a pool

        Args:
        ----
            network: Network id from `networks()` e.g. eth, solana, arbitrum
            pool_address: Address of pool
                e.g. 0x60594a405d53811d3bc4766596efd80fd545a270
            trade_volume_in_usd_greater_than: Trade volume in USD greater than
                e.g. 100000 (default 0)
        """
        return await self._get(
            endpoint=f"/networks/{network}/pools/{pool_address}/trades",
            params={
                "trade_volume_in_usd_greater_than": trade_volume_in_usd_greater_than,
            },
        )
