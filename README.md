[![Supported Versions](https://img.shields.io/pypi/pyversions/netrunner)](https://pypi.org/project/netrunner)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Netrunner
===

An async network command runner built using Scrapli.
You provide and inventory and tasks (functions), and the runner does the rest.

Currently only working with Cisco IOS and NXOS devices, but I will be adding others.

## Installation
---
```
pip install netrunner
```

## Basic Usage
---
Here is a basic example. More examples can be found in the examples folder.
```python
import asyncio

from netrunner import Runner

hosts = [
    {"hostname": "SW1021", "ip": "10.0.0.9", "platform": "ios"},
    {"hostname": "SW1031", "ip": "10.0.0.10", "platform": "ios"},
    {"hostname": "NX1001", "ip": "10.0.0.11", "platform": "nxos"},
    {"hostname": "NX2001", "ip": "10.0.0.12", "platform": "nxos"},
]


# Here is a task. The first parameter is the host and must be provided. Other parameters can also be passed into the tasks/functions. Please see the examples in the example folder.
async def first_task(host):
    # Commands must be passed in via a list. By default the output is parsed using
    # Genie, but parse can be set to False if raw output is required
    result = await host.send_command(cmds=["show version", "show vlan"])
    return result


async def main():
    # Hosts can either be passed here to be used globally, or can be passed per task
    runner = Runner(username="test_user", password="T3stpass", hosts=hosts)
    result = await runner.run(name="Check Version and Vlan", task=first_task)
    print(result.run_time)
    print(result.result["show version"])
    print(result.result["show vlan"])
    print(result.failed)


if __name__ == "__main__":
    asyncio.run(main())
```

