from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AddUserPage:
    def __init__(self, driver, base_url, timeout=5):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(f"{self.base_url}/add-user")

    def fill_form(self, name, age, gender, date_birthday, is_active):
        self.open()
        
        name_input = self.driver.find_element(By.ID, "name")
        name_input.clear()
        name_input.send_keys(name)

        age_input = self.driver.find_element(By.ID, "age")
        age_input.clear()
        age_input.send_keys(str(age))

        gender_input = self.driver.find_element(By.ID, "gender")
        gender_input.clear()
        gender_input.send_keys(gender)

        date_input = self.driver.find_element(By.ID, "date_birthday")
        date_input.clear()
        date_input.send_keys(date_birthday)

        checkbox = self.driver.find_element(By.ID, "isActive")
        if is_active and not checkbox.is_selected():
            checkbox.click()
        elif not is_active and checkbox.is_selected():
            checkbox.click()

    def submit_form(self):
        submit_btn = self.driver.find_element(By.ID, "add-btn")
        submit_btn.click()

    def fill_and_submit_form(self, name, age, gender, date_birthday, is_active):
        self.fill_form(name, age, gender, date_birthday, is_active)
        self.submit_form()

    def wait_for_error(self, error_id):
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, error_id))
        )

    def wait_for_success(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
        )
