import pytest
import requests
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://158.160.87.146:5000"

@pytest.fixture(scope="session")
def register_test_user():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "TestPassword123"

    # Регистрация
    reg_url = f"{BASE_URL}/api/register"
    reg_data = {"login": username, "password": password}
    reg_response = requests.post(reg_url, json=reg_data)
    print("Регистрация:", reg_response.status_code, reg_response.text)
    assert reg_response.status_code == 200
    assert reg_response.json().get("status") == "Successful"

    # Авторизация
    auth_url = f"{BASE_URL}/api/auth"
    auth_data = {"login": username, "password": password}
    auth_response = requests.post(auth_url, json=auth_data)
    print("Авторизация:", auth_response.status_code, auth_response.text)
    assert auth_response.status_code == 200

    try:
        token = auth_response.json().get("token")
    except Exception as e:
        pytest.fail(f"Ошибка разбора JSON токена: {e}\nОтвет: {auth_response.text}")

    assert token, "Токен не получен при авторизации"

    return {
        "username": username,
        "password": password,
        "token": token
    }

@pytest.fixture
def api_client(register_test_user):
    token = register_test_user["token"]

    class APIClient:
        def __init__(self, token):
            self.headers = {"Authorization": f"Bearer {token}"}

        def create_user(self, user_data):
            return requests.post(f"{BASE_URL}/api/user", json=user_data, headers=self.headers)

        def get_users(self):
            return requests.get(f"{BASE_URL}/api/users", headers=self.headers)

    return APIClient(token)

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Без открытия окна браузера
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get("http://158.160.87.146:5000")  # Адрес фронта

    yield driver

    driver.quit()

