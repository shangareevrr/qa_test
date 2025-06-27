from pages.add_user_page import AddUserPage

def test_add_user_positive(auth_driver, base_url):
    page = AddUserPage(auth_driver, base_url)
    page.fill_form("Том Марволо Реддл", 19, "М", "1926-01-31", True)
    page.submit_form()
    success_message = page.wait_for_success()
    assert "Пользователь успешно добавлен" in success_message.text

def test_add_user_missing_name(auth_driver, base_url):
    page = AddUserPage(auth_driver, base_url)
    page.fill_form("", 19, "М", "1994-01-01", True)
    page.submit_form()
    message = page.wait_for_error("nameError")
    assert "Поле обязательно" in message.text

def test_add_user_missing_age(auth_driver, base_url):
    page = AddUserPage(auth_driver, base_url)
    page.fill_form("Рон Уизли", "", "Ж", "1996-01-01", False)
    page.submit_form()
    message = page.wait_for_error("ageError")
    assert "Поле обязательно" in message.text

# если в будущем появится проверка gender, можно будет вернуть:
# def test_add_user_missing_gender(auth_driver, base_url):
#     page = AddUserPage(auth_driver, base_url)
#     page.fill_form("Гарри Поттер", 20, "", "1990-01-01", True)
#     page.submit_form()
#     message = page.wait_for_error("genderError")
#     assert "Поле обязательно" in message.text
