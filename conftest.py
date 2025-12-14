import pytest
from utils.api_client import ApiClient

@pytest.fixture 
def api_client(): 
    return ApiClient() 
