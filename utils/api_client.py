
import requests

BASE_URL = "https://stellarburgers.education-services.ru/api"

class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL

    def create_user(self, user_data):
        return requests.post(f"{self.base_url}/auth/register", json=user_data)

    def login(self, login_data):
        return requests.post(f"{self.base_url}/auth/login", json=login_data)

    def create_order(self, order_data, token=None):
        headers = {}
        if token:
            headers['Authorization'] = token
        return requests.post(f"{self.base_url}/orders", json=order_data, headers=headers)

    def get_ingredients(self):
        return requests.get(f"{self.base_url}/ingredients")
