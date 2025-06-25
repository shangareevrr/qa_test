from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def test_login_valid():
    # Инициализация драйвера с автоматической установкой chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://158.160.87.146:5000/login")

    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    password_input = driver.find_element(By.NAME, "password")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    username_input.send_keys("admin")
    password_input.send_keys("admin")
    submit_button.click()

    wait.until(lambda d: "Список пользователей" in d.page_source)
    
    driver.quit()
