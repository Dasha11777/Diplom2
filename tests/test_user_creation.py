
import pytest
from utils.api_client import ApiClient
from utils.helpers import generate_unique_user
import allure

client = ApiClient()

@allure.feature("User Creation")
@allure.story("Создание пользователя с заполненными всеми полями")
def test_create_unique_user():
    user = generate_unique_user()
    response = client.create_user(user)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("success") is True
    assert "accessToken" in json_data or "refreshToken" in json_data

@allure.feature("User Creation")
@allure.story("Создание пользователя с уже существующим email")
def test_create_duplicate_user():
    user = generate_unique_user()
    response1 = client.create_user(user)
    assert response1.status_code == 200
    response2 = client.create_user(user)
    assert response2.status_code == 403 or response2.status_code == 409
    assert response2.json()["message"] == "User already exists"

@allure.feature("User Creation")
@allure.story("Создание пользователя с пропущенным обязательным полем")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_create_user_missing_field(missing_field):
    user = generate_unique_user()
    user.pop(missing_field)
    response = client.create_user(user)
    assert response.status_code == 403 or response.status_code == 400
    assert response.json()["message"] == "Email, password and name are required fields"
