import pytest
from wc_client import WCClient


@pytest.fixture
def wc_client():
    return WCClient("example.com", "consumer_key", "consumer_secret")


# Test cases
def test_get_token(wc_client):
    token = wc_client._get_token()

    # auth token is base64 encoded 'consumer_key:consumer_secret'
    expected_token = "Basic Y29uc3VtZXJfa2V5OmNvbnN1bWVyX3NlY3JldA=="
    assert token == expected_token


def test_default_headers(wc_client):
    headers = wc_client._default_headers
    assert "Accept" in headers
    assert "User-Agent" in headers
    assert "Authorization" in headers


def test_getattr(wc_client):
    name = "products"
    wc_request = wc_client.__getattr__(name)
    assert wc_request.base_url == "example.com"
    assert wc_request.headers == wc_client._default_headers
