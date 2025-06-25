import pytest
import requests

@pytest.fixture(scope="session")
def get_token():
    url = "http://158.160.87.146:5000/api/auth"
    data = {"login": "admin", "password": "admin"}
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Failed to get token"
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    token = response.json().get("token")
    assert token, "Token not found in response"
    return token
