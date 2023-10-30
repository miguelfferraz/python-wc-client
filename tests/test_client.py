from wc_client import WCClient

URL = "https://api.domain.com"
KEY = "key"
SECRET = "secret"

mock_wc_client = WCClient(
    domain=URL,
    consumer_key=KEY,
    consumer_secret=SECRET
)


def test_build_url():
    builded_url = mock_wc_client._build_url("orders")

    assert builded_url == f"{URL}/orders"


def test_get_data(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "Mocked GET request"

    mocker.patch("httpx.get", return_value=mock_response)

    response = mock_wc_client.get("orders")

    assert response.status_code == 200
    assert response.text == "Mocked GET request"


def test_post_data(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.text = "Mocked POST request"

    mocker.patch("httpx.post", return_value=mock_response)

    response = mock_wc_client.post("orders", {"data": "data"})

    assert response.status_code == 201
    assert response.text == "Mocked POST request"
