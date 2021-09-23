import asyncio

from netrunner import Response, Runner
from netrunner.host import Host

ios_hosts = [
    {"hostname": "SW1021", "ip": "10.0.0.9", "platform": "ios"},
    {"hostname": "SW1031", "ip": "10.0.0.10", "platform": "ios"},
]

nxos_hosts = [
    {"hostname": "NX1001", "ip": "10.0.0.11", "platform": "nxos"},
    {"hostname": "NX2001", "ip": "10.0.0.12", "platform": "nxos"},
]


async def get_ip_ios(host: Host) -> dict:
    result = await host.send_command(["show ip interface brief"])
    return {"ip": result["show ip interface brief"]["interface"]["GigabitEthernet1/0"]["ip_address"]}


async def get_ip_nxos(host: Host, vrf: str) -> dict:
    result = await host.send_command([f"show ip interface vrf {vrf}"])
    return {
        "ip": result[f"show ip interface vrf {vrf}"]["mgmt0"]["ipv4"][
            next(iter(result[f"show ip interface vrf {vrf}"]["mgmt0"]["ipv4"]))
        ]["ip"]
    }


async def main():
    runner = Runner(username="test_user", password="T3stpass")
    runner.queue_task(name="ips for ios", task=get_ip_ios, hosts=ios_hosts)
    runner.queue_task(name="ips for nxos", task=get_ip_nxos, hosts=nxos_hosts, vrf="management")
    result: Response = await runner.run()
    print(f"run time: {result.run_time:.3f}")
    print(f"results for ips for ios task: {result.result['ips for ios']}")
    print(f"results for ips for nxos task: {result.result['ips for nxos']}")
    print(f"failed hosts: {result.failed}")


if __name__ == "__main__":
    asyncio.run(main())
