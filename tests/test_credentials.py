import pytest

from netrunner.runner import Credentials


def test_credentials_valid_no_enable():
    credentials = Credentials(username="test_user", password="test_pass")

    assert credentials.username == "test_user"
    assert credentials.password == "test_pass"
    assert credentials.enable == "test_pass"


def test_credentials_valid_with_enable():
    credentials = Credentials(username="test_user", password="test_pass", enable="test_enable")

    assert credentials.username == "test_user"
    assert credentials.password == "test_pass"
    assert credentials.enable == "test_enable"


def test_credentails_missing_value():
    with pytest.raises(TypeError):
        credentials = Credentials(password="test_pass")  # noqa: F841
