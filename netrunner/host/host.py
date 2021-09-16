from dataclasses import dataclass
from ipaddress import AddressValueError, IPv4Address
from typing import *  # noqa: F403
import random, asyncio

from netrunner.connections import SSH
from netrunner.connections.ssh import PLATFORM
from netrunner.host.errors import InvalidIPAddress, InvalidPlatform
from netrunner.runner import Credentials


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
        self.connection: SSH = SSH(
            host=ip,
            platform=platform,
            username=credentials.username,
            password=credentials.password,
            enable=credentials.enable,
        )

    def __repr__(self):
        return f"Host(Hostname: {self.hostname}, IP: {self.ip})"

    def __eq__(self, other):
        return all(
            [
                self.__class__ == other.__class__,
                self.ip == other.ip,
            ]
        )

    def __hash__(self):
        return hash(self.ip)

    async def send_command(self, cmds: list, parse: bool = True) -> Union[str, dict]:
        print("inside send")
        # async with self.connection.get_connection() as con:
        #     prompt = await self.connection._con.get_prompt()
        #     print(prompt)
        await self.connection.open()
        results = {cmd: await self.connection.send_command(cmd, parse) for cmd in cmds}
        return results


@dataclass
class FailedHost:
    hostname: str
    ip: IPv4Address
    task: str
    error: str
