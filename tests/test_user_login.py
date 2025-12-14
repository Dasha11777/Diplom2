from utils.helpers import generate_unique_user
import allure

class TestUserLogin:
    @allure.feature("User Login")
    @allure.title("Вход с существующим пользователем")
    def test_valid_user_login(self, api_client):
        with allure.step("Создание пользователя"):
            user = generate_unique_user()
            api_client.create_user(user)
        
        with allure.step("Вход пользователя"):
            login_data = {
                "email": user["email"],
                "password": user["password"]
            }
            response = api_client.login(login_data)

        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("success") is True
        assert "accessToken" in json_data

    @allure.feature("User Login")
    @allure.title("Вход с неверным логином и паролем")
    def test_invalid_user_login(self, api_client):
        with allure.step("Попытка входа с несуществующим пользователем"):
            user = generate_unique_user()
            # не создаем пользователя в системе
            login_data = {
                "email": user["email"],
                "password": user["password"]
            }
            response = api_client.login(login_data)
            
        assert response.status_code == 401
        assert "message" in response.json()
        assert response.json()["message"] == "email or password are incorrect"
