
import pytest
from utils.api_client import ApiClient
from utils.helpers import generate_unique_user
import allure

client = ApiClient()

@allure.feature("User Login")
@allure.story("Вход с существующим пользователем")
def test_valid_user_login():
    user = generate_unique_user()
    client.create_user(user)
    login_data = {
        "email": user["email"],
        "password": user["password"]
    }
    response = client.login(login_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("success") is True
    assert "accessToken" in json_data

@allure.feature("User Login")
@allure.story("Вход с неверным логином и паролем")
def test_invalid_user_login():    
    user = generate_unique_user()
    # не создаем пользователя в системе
    login_data = {
        "email": user["email"],
        "password": user["password"]
    }

    response = client.login(login_data)
    assert response.status_code == 401 or response.status_code == 403
    assert "message" in response.json()
    assert response.json()["message"] == "email or password are incorrect"
