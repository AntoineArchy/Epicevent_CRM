import unittest
from unittest.mock import patch, MagicMock

from utils import (
    is_valid_password,
    get_host_default_from_config,
    get_sentry_link_from_config,
    get_salt_from_config,
    hash_password,
)


def test_is_valid_password_valid():
    valid_password = "StrongP@ss123"
    result = is_valid_password(valid_password)
    assert result


def test_is_valid_password_invalid_length():
    invalid_password = "Short12"
    result = is_valid_password(invalid_password)
    assert not result


def test_is_valid_password_invalid_no_uppercase():
    invalid_password = "weakpassword123"
    result = is_valid_password(invalid_password)
    assert not result


def test_is_valid_password_invalid_no_lowercase():
    invalid_password = "WEAKPASSWORD123**"
    result = is_valid_password(invalid_password)
    assert not result


def test_is_valid_password_invalid_no_int():
    invalid_password = "weakPASSWORD**"
    result = is_valid_password(invalid_password)
    assert not result


def test_is_valid_password_invalid_space():
    invalid_password = "weak PASSWORD 123 **"
    result = is_valid_password(invalid_password)
    assert not result


def test_get_host_default_from_config_not_exists():
    result = get_host_default_from_config()

    assert result == "localhost"


def test_get_sentry_link_from_config_not_exists():
    result = get_sentry_link_from_config()

    assert not result
