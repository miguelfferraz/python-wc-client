from typing import Any, Dict

import httpx


class WCRequest:
    """
    A request builder for WooCommerce API.
    """

    METHODS = {"delete", "get", "patch", "post", "put"}

    def __init__(self, base_url: str, headers: Dict, *args):
        """
        Construct the WooCommerce request builder object.
            (e.g. WCRequest("https://example.com", {"Accept": "application/json"}, "consumer", "orders", "1"))

        Args:
            base_url (str): The base URL for the request
            headers (Dict): The headers for the request
            *args: The path for the request
        """
        self.base_url = base_url
        self.args = list(map(str, args))
        self.headers = headers

        self._url_path = [base_url]
        self._url_path.extend(self.args)

        self.client = httpx.Client(headers=headers)

    def _build_url(self) -> str:
        """
        Build the final URL for the request.

        Returns:
            str: The URL for the request
        """
        print(self._url_path)
        return "/".join(self._url_path)

    def _update_headers(self, headers):
        """
        Update the headers for the request.

        Args:
            headers (Dict): The headers to update
        """
        self.headers.update(headers)

    def _(self, resource: str) -> "WCRequest":
        """
        Build a new request with the given resource.

        Args:
            resource (str): The resource to append to the request

        Returns:
            WCRequest: The new request"""
        return WCRequest(self.base_url, self.headers, *self.args, resource)

    def __getattr__(self, resource: str) -> Any:
        """
        Adds method calls to the url path.
            (e.g. WCRequest().consumer.orders.get() -> {base_url}/consumer/orders/{variable})

        Args:
            resource (str): The resource to append to the request
        """
        if resource in self.METHODS:

            def make_request(body=None, query_params=None, headers=None):
                if headers:
                    self._update_headers(headers)

                return self.client.request(
                    method=resource,
                    url=self._build_url(),
                    data=body,
                    params=query_params,
                    headers=self.headers,
                )

            return make_request

        else:
            return self._(resource)
