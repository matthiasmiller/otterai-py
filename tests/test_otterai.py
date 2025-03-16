import os
from pprint import pprint
from unittest.mock import Mock

import pytest
import requests
from dotenv import load_dotenv

from otterai.otterai import OtterAI, OtterAIException

load_dotenv(dotenv_path=".env")

@pytest.fixture
def otterai_instance():
    return OtterAI()

def test_login(otterai_instance):
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")
    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otterai_instance.login(username, password)

    assert response["status"] == requests.codes.ok

def test_login_invalid_username(otterai_instance):
    # Use invalid username
    username = "invalid_username"
    password = os.getenv("OTTERAI_PASSWORD")
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otterai_instance.login(username, password)
    assert response["status"] != requests.codes.ok

def test_login_invalid_password(otterai_instance):
    # Use invalid password
    username = os.getenv("OTTERAI_USERNAME")
    password = "invalid_password"
    assert username is not None, "OTTERAI_USERNAME is not set in .env"

    response = otterai_instance.login(username, password)
    assert response["status"] != requests.codes.ok

def test_login_invalid_credentials(otterai_instance):
    # Use completely invalid credentials
    username = "invalid_username"
    password = "invalid_password"

    response = otterai_instance.login(username, password)
    assert response["status"] != requests.codes.ok

def test_is_userid_none():
    otter = OtterAI()
    assert otter._is_userid_invalid() is True

def test_is_userid_empty():
    otter = OtterAI()
    otter._userid = ""
    assert otter._is_userid_invalid() is True

def test_is_userid_valid():
    otter = OtterAI()
    otter._userid = "123456"
    assert otter._is_userid_invalid() is False

def test_handle_response_json(otterai_instance):
    # Mock response with JSON data
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.return_value = {"key": "value"}

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {"key": "value"}

def test_handle_response_no_json(otterai_instance):
    # Mock response without JSON data
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.side_effect = ValueError  # Simulate no JSON
    mock_response.text = "Some plain text"

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {}

def test_handle_response_with_data(otterai_instance):
    # Mock response with additional data passed
    mock_response = Mock()
    mock_response.status_code = 201
    additional_data = {"extra": "info"}

    result = otterai_instance._handle_response(mock_response, data=additional_data)
    assert result["status"] == 201
    assert result["data"] == additional_data

def test_get_user(otterai_instance):
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")

    response = otterai_instance.login(username, password)

    response = otterai_instance.get_user()
    pprint(response)

    assert response["status"] == requests.codes.ok