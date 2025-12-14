import pytest
from utils.helpers import generate_unique_user
import allure

class TestUserCreation:

    @allure.feature("User Creation")
    @allure.title("Создание пользователя с заполненными всеми полями")
    def test_create_unique_user(self, api_client):
        user = generate_unique_user()
        response = api_client.create_user(user)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("success") is True
        assert "accessToken" in json_data and "refreshToken" in json_data

    @allure.feature("User Creation")
    @allure.title("Создание пользователя с уже существующим email")
    def test_create_duplicate_user(self, api_client):

        with allure.step("Создание первого пользователя"):
            user = generate_unique_user()
            api_client.create_user(user)
        with allure.step("Создание второго пользователя с теми же данными"):
            response2 = api_client.create_user(user)

        assert response2.status_code == 403
        assert response2.json()["message"] == "User already exists"

    @allure.feature("User Creation")
    @allure.title("Создание пользователя с пропущенным обязательным полем")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, api_client, missing_field):
        user = generate_unique_user()
        user.pop(missing_field)
        response = api_client.create_user(user)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
