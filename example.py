import asyncio
from pprint import pprint

from netrunner.host import Host
from netrunner.runner import Response, Runner

devices = [
    {"hostname": "RT1001", "ip": "10.0.0.1", "platform": "ios"},
    {"hostname": "RT1002", "ip": "10.0.1.2", "platform": "ios"},
    {"hostname": "RT2001", "ip": "10.0.1.3", "platform": "ios"},
    {"hostname": "RT2002", "ip": "10.0.2.4", "platform": "ios"},
    # {"hostname": "RT1011", "ip": "10.0.0.5", "platform": "ios"},
    # {"hostname": "RT1021", "ip": "10.0.0.6", "platform": "ios"},
    #     {"hostname": "RT1031", "ip": "10.0.0.7", "platform": "ios"},
    #     {"hostname": "SW1011", "ip": "10.0.0.8", "platform": "ios"},
    #     {"hostname": "SW1021", "ip": "10.0.0.9", "platform": "ios"},
    #     {"hostname": "SW1031", "ip": "10.0.0.10", "platform": "ios"},
        {"hostname": "NX1001", "ip": "10.0.0.11", "platform": "nxos"},
        {"hostname": "NX2001", "ip": "10.0.0.12", "platform": "nxos"},
]

devices1 = [
    {"hostname": "SW1011", "ip": "10.0.0.8", "platform": "ios"},
    {"hostname": "SW1021", "ip": "10.0.0.9", "platform": "ios"},
    {"hostname": "SW1031", "ip": "10.0.0.10", "platform": "ios"},
    {"hostname": "NX1001", "ip": "10.0.0.11", "platform": "nxos"},
    {"hostname": "NX2001", "ip": "10.0.0.12", "platform": "nxos"},
]

devices2 = [
    {"hostname": "RT1011", "ip": "10.0.0.5", "platform": "ios"},
    {"hostname": "RT1021", "ip": "10.0.0.6", "platform": "ios"},
    {"hostname": "RT1031", "ip": "10.0.0.7", "platform": "ios"},
]


async def show_interfaces(host: Host):
    if host.platform == "nxos":
        result = await host.send_command(["show interface"])
    else:
        result = await host.send_command(["show interfaces"])
    return result


async def show_version(host: Host):
    result = await host.send_command(["show version"])
    return result


async def get_macs(host: Host):
    desktops = {}
    result = await host.send_command(["show mac address-table"])
    for key, value in result["show mac address-table"]["mac_table"]["vlans"]["10"]["mac_addresses"].items():
        desktops.update({key: {"interface": next(iter(value["interfaces"]))}})
    return desktops


async def main():

    runner = Runner(hosts=devices, username="ryan", password="Cisco123", debug=True)
    # runner = Runner(username="ryan", password="Cisco123", debug=True)
    # response = await runner.run(name="show interfaces", task=show_interfaces)
    # print(result)

    # pprint(result["RT1001"]["show interfaces"]["GigabitEthernet1"]["mac_address"])
    # print([f.__dict__ for f in failed])
    # runner.queue_task(name="show interfaces", task=show_interfaces, hosts=devices1)
    # runner.queue_task(name="show version", task=show_version, hosts=devices2)
    runner.queue_task(name="show interfaces", task=show_interfaces)
    runner.queue_task(name="show version", task=show_version)

    response: Response = await runner.run()
    # pprint(response.result["show interfaces"])
    # pprint(response.result["show version"])
    pprint(response.result.keys())
    pprint(response.failed)
    print(response.run_time)


if __name__ == "__main__":
    asyncio.run(main())
