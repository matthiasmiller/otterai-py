import json
import os
from datetime import datetime
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


@pytest.fixture
def authenticated_otterai_instance():
    otter = OtterAI()
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")

    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otter.login(username, password)
    assert response["status"] == requests.codes.ok, "Failed to log in"

    return otter


# Login Tests
def test_login(otterai_instance):
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")
    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otterai_instance.login(username, password)
    assert response["status"] == requests.codes.ok


def test_login_invalid_username(otterai_instance):
    response = otterai_instance.login("invalid_username", os.getenv("OTTERAI_PASSWORD"))
    assert response["status"] != requests.codes.ok


def test_login_invalid_password(otterai_instance):
    response = otterai_instance.login(os.getenv("OTTERAI_USERNAME"), "invalid_password")
    assert response["status"] != requests.codes.ok


def test_login_invalid_credentials(otterai_instance):
    response = otterai_instance.login("invalid_username", "invalid_password")
    assert response["status"] != requests.codes.ok


# User ID Validation Tests
def test_is_userid_none(otterai_instance):
    assert otterai_instance._is_userid_invalid() is True


def test_is_userid_empty(otterai_instance):
    otterai_instance._userid = ""
    assert otterai_instance._is_userid_invalid() is True


def test_is_userid_valid(otterai_instance):
    otterai_instance._userid = "123456"
    assert otterai_instance._is_userid_invalid() is False


# Response Handling Tests
def test_handle_response_json(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.return_value = {"key": "value"}

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {"key": "value"}


def test_handle_response_no_json(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.side_effect = ValueError  # Simulate no JSON
    mock_response.text = "Some plain text"

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {}


def test_handle_response_with_data(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = 201
    additional_data = {"extra": "info"}

    result = otterai_instance._handle_response(mock_response, data=additional_data)
    assert result["status"] == 201
    assert result["data"] == additional_data


# Authenticated Tests
def test_get_user(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_user()
    assert response["status"] == requests.codes.ok


def test_set_speech_title(authenticated_otterai_instance):
    speech_id = "aKD-fo-i-ulj4jY7VGschmV1nPo"

    response = authenticated_otterai_instance.get_speech(speech_id)

    title_after = f"Hello, World! {datetime.now()}"

    response = authenticated_otterai_instance.set_speech_title(
        speech_id=speech_id,
        title=title_after,
    )

    response = authenticated_otterai_instance.get_speech(speech_id)
    assert response["data"]["speech"]["title"] == title_after


def test_set_speech_title_invalid_userid(otterai_instance):
    otterai_instance._userid = None

    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.set_speech_title("speech_id", "New Title")


def test_get_speakers_success(authenticated_otterai_instance):
    result = authenticated_otterai_instance.get_speakers()
    assert result["status"] == requests.codes.ok
    assert "speakers" in result["data"]
    assert isinstance(result["data"]["speakers"], list)


def test_get_speakers_invalid_userid(otterai_instance):
    otterai_instance._userid = None

    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speakers()


def test_get_speeches_invalid_userid(otterai_instance):
    otterai_instance._userid = None

    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speeches()


def test_get_speeches_success(authenticated_otterai_instance):
    result = authenticated_otterai_instance.get_speeches()
    assert result["status"] == requests.codes.ok
    assert "speeches" in result["data"]
    assert isinstance(result["data"]["speeches"], list)


def test_get_speech_success(authenticated_otterai_instance):
    speech_id = "aKD-fo-i-ulj4jY7VGschmV1nPo"
    response = authenticated_otterai_instance.get_speech(speech_id)
    assert response["status"] == requests.codes.ok
    assert "speech" in response["data"]
    assert response["data"]["speech"]["otid"] == speech_id


def test_get_speech_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speech("invalid_speech_id")
