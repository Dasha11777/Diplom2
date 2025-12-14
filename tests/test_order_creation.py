from utils.helpers import generate_unique_user
import allure

class TestOrderCreation:

    @allure.feature("Order Creation")
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, api_client):
        with allure.step("Создание пользователя и получение токена"):
            user = generate_unique_user()
            api_client.create_user(user)
            login_response = api_client.login({"email": user["email"], "password": user["password"]})
            token = login_response.json().get("accessToken")

        with allure.step("Получение списка ингредиентов"):
            ingredients_resp = api_client.get_ingredients()
            ingredients_list = ingredients_resp.json().get("data")
            ingredient_ids = [ingredient['_id'] for ingredient in ingredients_list[:2]]

        with allure.step("Создание заказа с ингредиентами"):
            order_data = {"ingredients": ingredient_ids}
            response = api_client.create_order(order_data, token)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.feature("Order Creation")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_client):
        with allure.step("Получение списка ингредиентов"):
            ingredients_resp = api_client.get_ingredients()
            ingredient_ids = [ingredient['_id'] for ingredient in ingredients_resp.json().get("data")[:1]]

        with allure.step("Создание заказа без токена"):    
            order_data = {"ingredients": ingredient_ids}
            response = api_client.create_order(order_data)

        assert response.status_code == 401

    @allure.feature("Order Creation")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client):        
        with allure.step("Создание пользователя и получение токена"):
            user = generate_unique_user()
            api_client.create_user(user)
            login_response = api_client.login({"email": user["email"], "password": user["password"]})
            token = login_response.json().get("accessToken")

        with allure.step("Создание заказа без ингредиентов"):    
            order_data = {"ingredients": []}
            response = api_client.create_order(order_data, token)

        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.feature("Order Creation")
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, api_client):
        with allure.step("Создание пользователя и получение токена"):
            user = generate_unique_user()
            api_client.create_user(user)
            login_response = api_client.login({"email": user["email"], "password": user["password"]})
            token = login_response.json().get("accessToken")

        with allure.step("Создание заказа с неверным хешем ингредиентов"):
            order_data = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}
            response = api_client.create_order(order_data, token)
            
        assert response.status_code == 500
