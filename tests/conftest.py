import pytest

from netrunner.connections import SSH
from netrunner.host import Host
from netrunner.runner.credentials import Credentials


@pytest.fixture()
def ssh_obj() -> SSH:
    return SSH(host="10.0.0.1", username="test_user", password="test_pass", enable="test_enable", platform="ios")


@pytest.fixture()
def host_obj() -> Host:
    return Host(
        hostname="RT001",
        ip="10.0.0.1",
        platform="ios",
        credentials=Credentials(username="test_user", password="test_pass"),
    )
