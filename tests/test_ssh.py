import pytest

from scrapli.driver.core import AsyncIOSXEDriver, AsyncNXOSDriver
from scrapli.driver import AsyncNetworkDriver

from netrunner.connections import SSH


def test_obj_init_pass(ssh_obj):
    assert ssh_obj.host == "10.0.0.1"
    assert ssh_obj.username == "test_user"
    assert ssh_obj.password == "test_pass"
    assert ssh_obj.enable == "test_enable"
    assert ssh_obj.platform == "ios"
    assert ssh_obj._con == None


def test_obj_init_missing_params():
    with pytest.raises(TypeError):
        connection = SSH(host="10.0.0.1", password="test_pass", enable="test_enable", platform="ios")


@pytest.mark.parametrize("platform, platform_obj", [["ios", AsyncIOSXEDriver], ["nxos", AsyncNXOSDriver]])
def test_get_driver(platform, platform_obj):
    connection = SSH(
        host="10.0.0.1", username="test_user", password="test_pass", enable="test_enable", platform=platform
    )
    connection.get_driver()
    assert isinstance(connection._con, platform_obj)


@pytest.mark.parametrize("response", [True, False])
def test_is_alive(ssh_obj, monkeypatch, response):
    def mock_isalive(cls):
        return response

    monkeypatch.setattr(AsyncNetworkDriver, "isalive", mock_isalive)

    ssh_obj.get_driver()
    assert ssh_obj.is_alive == response
