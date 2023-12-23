import requests

from .exceptions import GeckoTerminalAPIError


class GeckoTerminalAPI:
    """RESTful Python client for GeckoTerminal API. """

    def __init__(self, api_version: str | None = None):
        """
        Args:
            api_version: GeckoTerminal API version, if None latest will be used
        """

        super().__init__()
        self.api_version = api_version
        self._base_url = "https://api.geckoterminal.com/api/v2/"
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
