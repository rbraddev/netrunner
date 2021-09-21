import pytest
from scrapli.driver.network import AsyncNetworkDriver

from netrunner.host import Host
from netrunner.host.errors import InvalidPlatform, InvalidIPAddress
from netrunner.runner import Credentials
from netrunner.connections import SSH


def test_host_obj_init_pass():
    host = Host(
        hostname="RT001",
        ip="10.0.0.1",
        platform="ios",
        credentials=Credentials(username="test_user", password="test_pass"),
    )

    assert host.hostname == "RT001"
    assert host.ip == "10.0.0.1"
    assert host.platform == "ios"
    assert host.credentials.username == "test_user"
    assert host.credentials.password == "test_pass"


def test_host_obj_invalid_platform():
    with pytest.raises(InvalidPlatform):
        host = Host(
            hostname="RT001",
            ip="10.0.0.1",
            platform="invalid_platform",
            credentials=Credentials(username="test_user", password="test_pass"),
        )


def test_host_obj_invalid_ip():
    with pytest.raises(InvalidIPAddress):
        host = Host(
            hostname="RT001",
            ip="not an ip",
            platform="ios",
            credentials=Credentials(username="test_user", password="test_pass"),
        )


def test_host_obj_equality(host_obj):
    host1 = host_obj
    host2 = Host(
        hostname="RT001",
        ip="10.0.0.1",
        platform="ios",
        credentials=Credentials(username="test_user", password="test_pass"),
    )
    assert host1 == host2


def test_host_obj_inequality(host_obj):
    host2 = Host(
        hostname="RT002",
        ip="10.0.0.2",
        platform="ios",
        credentials=Credentials(username="test_user", password="test_pass"),
    )
    assert host_obj != host2


def test_host_set_connection(host_obj):
    host_obj.set_connection(task_name="test task")
    assert "test task" in host_obj.connections.keys()
    assert isinstance(host_obj.connections["test task"], SSH)


@pytest.mark.asyncio
async def test_host_send_command(host_obj: Host, monkeypatch: pytest.MonkeyPatch):
    async def mock_send_command(cls, cmd, parse):
        return f"{cmd} output"

    def mock_isalive(cls):
        return True

    monkeypatch.setattr(AsyncNetworkDriver, "isalive", mock_isalive)
    monkeypatch.setattr(SSH, "send_command", mock_send_command)

    host_obj.set_connection(task_name="test task")
    result = await host_obj.send_command(
        ["show version", "show interface status"], parse=True, connection=host_obj.connections["test task"]
    )

    assert result == {
        "show version": "show version output",
        "show interface status": "show interface status output"
    }
