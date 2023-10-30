import base64
from typing import Dict

import httpx


class WCClient:
    """
    A client for interacting with a WooCommerce store.
    """

    def __init__(self, domain: str, consumer_key: str, consumer_secret: str):
        self.domain = domain
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def _authenticate(self) -> str:
        """
        Returns the authentication token.

        Returns:
            Tuple[str, str]: The authentication token
        """
        auth_str = f"{self.consumer_key}:{self.consumer_secret}"
        enconded_auth = base64.b64encode(auth_str.encode("utf-8")).decode(
            "utf-8"
        )
        return f"Basic {enconded_auth}"

    def _build_headers(self, headers: Dict = None) -> Dict[str, str]:
        """
        Returns the headers for the request, including the Authorization

        Args:
            headers (Dict): The headers to be added

        Returns:
            Dict: The headers
        """
        updated_headers = {} if headers is None else headers.copy()

        updated_headers["Accept"] = "application/json"
        updated_headers["User-Agent"] = "WooCommerce-Python-REST-API/wc/v3"
        updated_headers["Authorization"] = self._authenticate()

        return updated_headers

    def _build_url(self, endpoint: str) -> str:
        """
        Returns the full url for the endpoint

        Args:
            endpoint (str): The endpoint to be called

        Returns:
            str: The full url
        """
        return f"{self.domain}/{endpoint}"

    def get(self, endpoint: str, headers: Dict = {}) -> httpx.Response:
        """
        Perform a GET request to the specified endpoint

        Args:
            endpoint (str): The endpoint to retrieve data from
            headers (Dict): Additional headers to include in the request

        Returns:
            httpx.Response: The HTTP response
        """
        return httpx.get(
            url=self._build_url(endpoint), headers=self._build_headers(headers)
        )

    def post(
        self, endpoint: str, data: Dict, headers: Dict = {}
    ) -> httpx.Response:
        """
        Perform a POST request to the specified endpoint

        Args:
            endpoint (str): The endpoint to post data to
            data (Dict): The data to be posted
            headers (Dict): Additional headers to include in the request

        Returns:
            httpx.Response: The HTTP response
        """
        return httpx.post(
            url=self._build_url(endpoint),
            headers=self._build_headers(headers),
            json=data,
        )
