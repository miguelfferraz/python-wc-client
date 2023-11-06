from unittest.mock import MagicMock
from wc_client.request import WCRequest  # Import your WCRequest class


# Mocked response for HTTP request
class MockResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


def test_build_url():
    request = WCRequest(
        "https://example.com",
        {"Accept": "application/json"},
        "consumer",
        "orders",
        "1",
    )
    expected_url = "https://example.com/consumer/orders/1"
    assert request._build_url() == expected_url


def test_update_headers():
    request = WCRequest(
        "https://example.com",
        {"Accept": "application/json"},
        "consumer",
        "orders",
        "1",
    )
    request._update_headers({"Authorization": "Bearer token"})
    expected_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer token",
    }
    assert request.headers == expected_headers


def test_make_request():
    # Mocking httpx.Client.request
    client = MagicMock()
    client.request.return_value = MockResponse(b'{"key": "value"}', 200)
    request = WCRequest(
        "https://example.com",
        {"Accept": "application/json"},
        "consumer",
        "orders",
        "1",
    )
    request.client = client

    response = request.get(
        body=None,
        query_params=None,
        headers={"Authorization": "foo-bar"},  # update headers
    )

    client.request.assert_called_once_with(
        method="get",
        url="https://example.com/consumer/orders/1",
        data=None,
        params=None,
        headers={
            "Accept": "application/json",
            "Authorization": "foo-bar",
        },  # assert updated headers
    )
    assert response.status_code == 200
    assert response.content == b'{"key": "value"}'


def test_chained_calls():
    request = WCRequest("https://example.com", {"Accept": "application/json"})
    new_request = request.consumer.orders
    expected_url = "https://example.com/consumer/orders"
    assert new_request._build_url() == expected_url

    new_request = new_request._(1)
    expected_url = "https://example.com/consumer/orders/1"
    assert new_request._build_url() == expected_url

    new_request = new_request.details
    expected_url = "https://example.com/consumer/orders/1/details"
    assert new_request._build_url() == expected_url
