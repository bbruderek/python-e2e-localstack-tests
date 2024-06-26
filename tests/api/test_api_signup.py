import pytest
from api.post_sign_up import SignUp
from dotenv import load_dotenv
import requests
from generators.user_generator import get_random_user

load_dotenv()

@pytest.fixture
def sign_up_api():
    return SignUp()

def test_successful_api_signup(sign_up_api: SignUp):
    user = get_random_user()
    response = sign_up_api.api_call(user)
    try:
        response.raise_for_status()
        assert response.status_code == 201, "Expected status code 201 for successful registration"
        assert response.json()['token'] is not None, "Token should not be None in the response"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")
        
def test_return_400_if_email_is_empty(sign_up_api: SignUp):
    user = get_random_user()
    user.email = ""
    try:
        sign_up_api.api_call(user)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "email" in e.response.json(), "Expected error message for missing email"
        
def test_return_403_if_access_token_is_empty(sign_up_api: SignUp):
    user = get_random_user()
    user.access_token = ""
    try:
        sign_up_api.api_call(user)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 403, "Expected status code 403"
        assert "Access denied" in e.response.json(), "Expected error message for missing access token"
        
def test_return_422_if_username_already_exists(sign_up_api: SignUp):
    user = get_random_user()
    sign_up_api.api_call(user)
    try:
        sign_up_api.api_call(user)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 422, "Expected status code 422"
        assert "Username is already in use" == e.response.json()["message"], "Expected error message for existing username"
