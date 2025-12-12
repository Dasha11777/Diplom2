
import pytest
from utils.api_client import ApiClient
from utils.helpers import generate_unique_user
import allure

client = ApiClient()

@allure.feature("Order Creation")
@allure.story("Создание заказа с авторизацией и ингредиентами")
def test_create_order_with_auth_and_ingredients():
    user = generate_unique_user()
    client.create_user(user)
    login_response = client.login({"email": user["email"], "password": user["password"]})
    token = login_response.json().get("accessToken")

    ingredients_resp = client.get_ingredients()
    assert ingredients_resp.status_code == 200
    ingredients_list = ingredients_resp.json().get("data")
    ingredient_ids = [ingredient['_id'] for ingredient in ingredients_list[:2]]

    order_data = {"ingredients": ingredient_ids}

    response = client.create_order(order_data, token)
    assert response.status_code == 200
    assert response.json().get("success") is True

@allure.feature("Order Creation")
@allure.story("Создание заказа без авторизации")
def test_create_order_without_auth():
    ingredients_resp = client.get_ingredients()
    ingredient_ids = [ingredient['_id'] for ingredient in ingredients_resp.json().get("data")[:1]]
    order_data = {"ingredients": ingredient_ids}

    response = client.create_order(order_data)
    assert response.status_code == 401 or response.status_code == 403

@allure.feature("Order Creation")
@allure.story("Создание заказа без ингредиентов")
def test_create_order_without_ingredients():
    user = generate_unique_user()
    client.create_user(user)
    login_response = client.login({"email": user["email"], "password": user["password"]})
    token = login_response.json().get("accessToken")

    order_data = {"ingredients": []}
    response = client.create_order(order_data, token)
    assert response.status_code == 400 or response.status_code == 422
    assert response.json()["message"] == "Ingredient ids must be provided"

@allure.feature("Order Creation")
@allure.story("Создание заказа с неверным хешем ингредиентов")
def test_create_order_with_invalid_ingredients():
    user = generate_unique_user()
    client.create_user(user)
    login_response = client.login({"email": user["email"], "password": user["password"]})
    token = login_response.json().get("accessToken")

    order_data = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}
    response = client.create_order(order_data, token)
    assert response.status_code == 500 or response.status_code == 400
