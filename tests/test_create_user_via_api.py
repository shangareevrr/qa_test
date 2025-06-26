# tests/test_create_user_via_api.py

def create_user_and_assert(api_client, user_data, expected_status, label=""):
    """Создаёт пользователя и проверяет статус ответа."""
    response = api_client.create_user(user_data)

    error_messages = {
        "Negative age": "Пользователь создался с отрицательным возрастом (ожидалась ошибка 400, пришёл 200).",
        "String age": "Пользователь создался с возрастом в виде строки (ожидалась ошибка 400, пришёл 200).",
        "Invalid gender": "Пользователь создался с некорректным значением пола (ожидалась ошибка 400, пришёл 200).",
        "No gender": "Пользователь создался с пустым значением пола (ожидалась ошибка 400, пришёл 200).",
        "No is_active": "Не удалось создать пользователя без поля is_active (ожидался статус 200, пришёл 400).",
        "Combined errors": "Пользователь с несколькими ошибками (например, пустое имя и отрицательный возраст) был успешно создан (ожидалась ошибка 400, пришёл 200).",
        "Long name": "Пользователь с очень длинным именем был успешно создан (ожидалась ошибка 400, пришёл 200)."
    }

    message = error_messages.get(label, f"{label}: ожидался статус {expected_status}, получен {response.status_code}")
    assert response.status_code == expected_status, message


def test_create_user_negative_age(api_client):
    user = {
        "name": "Гарри Поттер",
        "age": -1,
        "gender": "М",
        "date_registration": "1980-07-31",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 400, "Negative age")


def test_create_user_string_age(api_client):
    user = {
        "name": "Рон Уизли",
        "age": "семнадцать",
        "gender": "М",
        "date_registration": "1980-03-01",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 400, "String age")


def test_create_user_invalid_gender(api_client):
    user = {
        "name": "Драко Малфой",
        "age": 42,
        "gender": "X",
        "date_registration": "1980-06-05",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 400, "Invalid gender")


def test_create_user_no_gender(api_client):
    user = {
        "name": "Луна Лавгуд",
        "age": 42,
        "gender": "",
        "date_registration": "1981-02-13",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 400, "No gender")


def test_create_user_no_is_active(api_client):
    user = {
        "name": "Сириус Блэк",
        "age": 42,
        "gender": "М",
        "date_registration": "1981-11-03"
    }
    create_user_and_assert(api_client, user, 200, "No is_active")


def test_create_user_combined_errors(api_client):
    user = {
        "name": "",
        "age": -5,
        "gender": "М",
        "date_registration": "1980-12-24",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 400, "Combined errors")


def test_create_user_long_name(api_client):
    user = {
        "name": "Гермиона Джин Джаневра Мальсибер-Снейп-Лестрейндж",
        "age": 42,
        "gender": "Ж",
        "date_registration": "1979-09-19",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 400, "Long name")


def test_create_user_valid(api_client):
    user = {
        "name": "Невилл Долгопупс",
        "age": 42,
        "gender": "М",
        "date_registration": "1980-07-30",
        "is_active": True
    }
    create_user_and_assert(api_client, user, 200, "Valid user")


def test_create_user_missing_optional_field(api_client):
    user = {
        "name": "Чжоу Чанг",
        "age": 41,
        "gender": "Ж",
        "date_registration": "1980-02-02"
    }
    create_user_and_assert(api_client, user, 200, "Missing is_active field")


def test_create_user_minimal_valid_data(api_client):
    user = {
        "name": "Дин Томас",
        "age": 43,
        "gender": "М",
        "date_registration": "1981-01-01",
        "is_active": False
    }
    create_user_and_assert(api_client, user, 200, "Minimal valid data")
