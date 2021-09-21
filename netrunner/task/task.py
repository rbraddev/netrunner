import asyncio
from typing import *  # noqa: F403

from netrunner.host import FailedHost, Host
from netrunner.runner import Response


class Task:
    def __init__(self, task: Callable, name: str, hosts: List[Host], response: Response, params: dict = None) -> None:
        self.task: Callable = task
        self.name: str = name
        self.hosts: List[Host] = hosts
        self.params: dict = params
        self.debug: bool = False
        self.response: Response = response

    async def _run_task(self, host: Host):
        if self.debug:
            print(f"Starting task for {host.hostname}")
        try:
            host.set_connection(task_name=self.task.__name__)
            result = (
                await asyncio.create_task(self.task(host, **self.params))
                if self.params
                else await asyncio.create_task(self.task(host))
            )
            await host.connections.get(self.task.__name__).close()
            self.response.result[self.name].update({host.hostname: result})
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.response.failed.append(FailedHost(host.hostname, host.ip, self.name, getattr(e, "message", str(e))))

    async def run_task(self, debug: bool):
        """Starts the task running"""
        self.debug = debug
        self.response.result.update({self.name: {}})
        await asyncio.gather(*[self._run_task(host) for host in self.hosts], return_exceptions=True)
