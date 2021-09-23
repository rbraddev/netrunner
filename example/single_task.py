import asyncio

from netrunner import Response, Runner
from netrunner.host import Host

hosts = [
    {"hostname": "SW1021", "ip": "10.0.0.9", "platform": "ios"},
    {"hostname": "SW1031", "ip": "10.0.0.10", "platform": "ios"},
    {"hostname": "NX1001", "ip": "10.0.0.11", "platform": "nxos"},
    {"hostname": "NX2001", "ip": "10.0.0.12", "platform": "nxos"},
]


def get_version(platform, result):
    if platform == "ios":
        version = result["version"]["version_short"]
    if platform == "nxos":
        version = result["platform"]["software"]["system_version"]
    return version


async def task1(host: Host, vlan: str):
    result = await host.send_command(cmds=["show version", "show vlan"])
    return {
        "version": get_version(host.platform, result["show version"]),
        "vlan_present": vlan in result["show vlan"]["vlans"].keys(),
    }


async def main():
    runner = Runner(username="test_user", password="T3stpass", hosts=hosts)
    result: Response = await runner.run(name="Check Version and Vlan", task=task1, vlan="10")
    print(result.run_time)
    print(result.result)
    print(result.failed)


if __name__ == "__main__":
    asyncio.run(main())
