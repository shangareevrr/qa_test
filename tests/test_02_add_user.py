import requests

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
