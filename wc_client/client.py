import base64
from typing import Dict

from wc_client.request import WCRequest


class WCClient:
    """
    A client for interacting with a WooCommerce API.
    """

    def __init__(self, domain: str, consumer_key: str, consumer_secret: str):
        self.domain = domain
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def _get_token(self) -> str:
        """
        Returns the authentication token.

        Returns:
            str: The authentication token
        """
        auth_str = f"{self.consumer_key}:{self.consumer_secret}"
        enconded_auth = base64.b64encode(auth_str.encode("utf-8")).decode(
            "utf-8"
        )
        return f"Basic {enconded_auth}"

    @property
    def _default_headers(self) -> Dict[str, str]:
        """
        Set the default headers for WooCommerce API call

        Returns:
            Dict: The headers
        """
        return {
            "Accept": "application/json",
            "User-Agent": "WooCommerce-Python-REST-API/wc/v3",
            "Authorization": self._get_token(),
        }

    def __getattr__(self, name):
        return WCRequest(self.domain, self._default_headers, name)
