import functools
import inspect
from dataclasses import dataclass
from ipaddress import AddressValueError, IPv4Address
from typing import *  # noqa: F403

from netrunner.connections import SSH
from netrunner.connections.ssh import PLATFORM
from netrunner.host.errors import InvalidIPAddress, InvalidPlatform
from netrunner.runner import Credentials


def connection_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if "connection" not in kwargs.keys():
            function_list = [f.function for f in inspect.getouterframes(inspect.currentframe())]
            kwargs["connection"] = args[0].connections.get(function_list[function_list.index("_run") - 1])
        await kwargs["connection"].open()
        result = await func(*args, **kwargs)
        return result

    return wrapper


class Host:
    def __init__(self, hostname: str, ip: str, platform: str, credentials: Credentials) -> None:
        if platform not in PLATFORM.keys():
            raise InvalidPlatform(f"Host {hostname}: platform must be {list(PLATFORM.keys())}")
        self.hostname: str = hostname
        try:
            self.ip: str = str(IPv4Address(ip))
        except AddressValueError:
            raise InvalidIPAddress(f"Host: {hostname} - has an invalid ip address of {ip}")
        self.platform: str = platform
        self.credentials: Credentials = credentials
        self.connections: Dict[str, SSH] = {}

    def __repr__(self) -> str:
        return f"Host(Hostname: {self.hostname}, IP: {self.ip})"

    def __eq__(self, other) -> bool:
        return all(
            [
                self.__class__ == other.__class__,
                self.ip == other.ip,
            ]
        )

    def __hash__(self):
        return hash(self.ip)

    def set_connection(self, task_name: str):
        self.connections.update(
            {
                task_name: SSH(
                    host=self.ip,
                    username=self.credentials.username,
                    password=self.credentials.password,
                    enable=self.credentials.enable,
                    platform=self.platform,
                )
            }
        )

    @connection_required
    async def send_command(self, cmds: list, parse: bool = True, connection: SSH = None) -> Union[str, dict]:
        results = {cmd: await connection.send_command(cmd, parse) for cmd in cmds}
        return results


@dataclass
class FailedHost:
    hostname: str
    ip: IPv4Address
    task: str
    error: str
