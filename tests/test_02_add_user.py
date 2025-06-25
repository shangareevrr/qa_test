import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ---------- ФИКСТУРЫ ----------

@pytest.fixture(scope="session")
def get_token():
    url = "http://158.160.87.146:5000/api/auth"
    data = {"login": "admin", "password": "admin"}
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Failed to get token"
    token = response.json().get("token")
    assert token, "Token not found in response"
    return token


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # устранение DirectComposition ошибки

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 1. Авторизация через UI
    driver.get("http://158.160.87.146:5000/login")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "login"))).send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, 5).until(lambda d: "Список пользователей" in d.page_source)

    # 2. Переход к форме добавления
    driver.get("http://158.160.87.146:5000/add-user")

    yield driver
    driver.quit()

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------

def fill_form(driver, name, age, gender, date, is_active):
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "age").send_keys(str(age))
    driver.find_element(By.NAME, "gender").send_keys(gender)
    driver.find_element(By.NAME, "date_birthday").send_keys(date)  # ← корректное имя поля
    if is_active:
        driver.find_element(By.NAME, "is_active").click()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

def get_message(driver):
    return WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "messageContainer"))
    ).text

def wait_for_error(driver, element_id, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )

# ---------- UI-ТЕСТЫ ----------
# пропущено имя
def test_add_user_missing_name(driver):
    fill_form(driver, "", 19, "М", "1994-01-01", True)
    message = wait_for_error(driver, "nameError")
    assert "Поле обязательно" in message.text
# пропущен возраст
def test_add_user_missing_age(driver):
    fill_form(driver, "Уизли", "", "Ж", "1996-01-01", False)
    message = wait_for_error(driver, "ageError")
    assert "Поле обязательно" in message.text
# Отрицательное число в возрасте
def test_add_user_invalid_age_low(driver):
    fill_form(driver, "Малфой", -10, "М", "1900-01-01", True)
#    assert "ошибка" in get_message(driver).lower()
# слишком большое число в поле возраст
def test_add_user_invalid_age_high(driver):
    fill_form(driver, "Ктулху", 10000, "М", "1000-12-12", False)
#    assert "ошибка" in get_message(driver).lower()
# не валидный пол
def test_add_user_invalid_gender(driver):
    fill_form(driver, "Джон", 30, "мужчина", "1990-05-05", True)
#    assert "ошибка" in get_message(driver).lower()
# пустой пользователь
def test_add_invisible_man(driver):
    fill_form(driver, "", 0, "", "", True)
    assert "Поле обязательно" in message.text
# не корректный возраст
def test_add_invisible_man(driver):
    fill_form(driver, "Дамболдор", 0, "", "111111111111", True)



# ---------- API-ТЕСТ ----------

def test_add_user(get_token):
    url = "http://158.160.87.146:5000/api/user"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    payload = {
        "name": "Поттер",
        "age": 25,
        "gender": "М",
        "date_registration": "1994-01-01",
        "is_active": True
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Status code:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "Successful"
