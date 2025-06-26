import pytest
from pages.add_user_page import AddUserPage

def test_add_user_missing_name(driver):
    page = AddUserPage(driver)
    page.open()
    page.fill_form("", 19, "М", "1994-01-01", True)
    page.submit_form()
    message = page.wait_for_error("nameError")
    assert "Поле обязательно" in message.text

def test_add_user_missing_age(driver):
    page = AddUserPage(driver)
    page.open()
    page.fill_form("Рон Уизли", "", "Ж", "1996-01-01", False)
    page.submit_form()
    message = page.wait_for_error("ageError")
    assert "Поле обязательно" in message.text

def test_add_user_missing_gender(driver):
    page = AddUserPage(driver)
    page.open()
    page.fill_form("Гарри Поттер", 20, "", "1990-01-01", True)
    page.submit_form()
    message = page.wait_for_error("genderError")
    assert "Поле обязательно" in message.text
