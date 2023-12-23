import warnings
from typing import Optional

import requests

from .exceptions import GeckoTerminalAPIError, GeckoTerminalParameterWarning


class GeckoTerminalAPI:
    """RESTful Python client for GeckoTerminal API."""

    def __init__(self, api_version: str | None = None):
        """
        Args:
            api_version: GeckoTerminal API version, if None latest will be used
        """
        self.api_version = api_version
        self._base_url = "https://api.geckoterminal.com/api/v2"
        self._session = requests.Session()

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        if self.api_version:
            accept_header = f"application/json;version={self.api_version}"
        else:
            accept_header = "application/json"
        headers = {
            "accept": accept_header,
        }
        url = self._base_url + endpoint
        response = self._session.request(
            method="GET", url=url, params=params, headers=headers, timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise GeckoTerminalAPIError(status=response.status_code, err=response.text)

    @staticmethod
    def _validate_page(f, *args, **kwargs):
        if "page" in kwargs and kwargs["page"] > 10:
            warnings.warn(
                f"Maximum 10 pages allowed, {kwargs['page']} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    @staticmethod
    def _validate_addresses(f, *args, **kwargs):
        if len(args[1]) > 30:
            warnings.warn(
                f"Maximum 30 addresses allowed, {len(args[1])} provided",
                GeckoTerminalParameterWarning,
                stacklevel=2,
            )
        return f(*args, **kwargs)

    def networks(self, page: int = 1) -> dict:
        """Get list of supported networks

        Args:
            page: Page through results (default 1)
        """
        return self._get(endpoint="/networks", params={"page": page})

    def dexes(self, network: str, page: int = 1) -> dict:
        """Get list of supported dexes on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
            page: Page through results (default 1)
        """
        return self._get(endpoint=f"/networks/{network}/dexes", params={"page": page})

    @_validate_page
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

    @_validate_page
    def network_trending_pools(
        self, network: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get trending pools on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
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

    def network_pool_address(
        self,
        network: str,
        address: str,
        include: Optional[list] = None,
    ) -> dict:
        """Get specific pool on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
            address: Address of pool
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

    @_validate_addresses
    def network_pools_multi_address(
        self, network: str, addresses: list[str], include: Optional[list] = None
    ) -> dict:
        """Get multiple pools on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
            addresses: List of pool addresses
                e.g. ["0x60594a405d53811d3bc4766596efd80fd545a270",
                "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"]
            include: List of related resources to include in response. Available
                resources are: base_token, quote_token, dex (default all)
        """
        if include is None:
            include = ["base_token", "quote_token", "dex"]
        return self._get(
            endpoint=f"/networks/{network}/pools/multi/{'%'.join(addresses)}",
            params={
                "include": ",".join(include),
            },
        )

    def network_pools(
        self, network: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get top pools on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
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

    def network_dex_pools(
        self, network: str, dex: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get top pools on a network's dex

        Args:
            network: Network id from `networks()` e.g. "eth"
            dex: Dex id from `dexes()` e.g. "uniswap"
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

    @_validate_page
    def network_new_pools(
        self, network: str, include: Optional[list] = None, page: int = 1
    ) -> dict:
        """Get new pools on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
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

    @_validate_page
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

    @_validate_page
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
            network: Network id from `networks()` e.g. "eth"
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

    @_validate_addresses
    def network_addresses_token_price(self, network: str, addresses: list[str]) -> dict:
        """Get current USD prices of multiple tokens on a network

        Args:
            network: Network id from `networks()` e.g. "eth"
            addresses: List of token addresses
                e.g. ["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"]
        """
        return self._get(
            endpoint=f"/simple/networks/{network}/token_price/{'%'.join(addresses)}",
        )
