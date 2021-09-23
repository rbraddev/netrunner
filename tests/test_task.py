from typing import *  # noqa: F403

from netrunner.host import Host
from netrunner.runner import Response
from netrunner.task import Task


def test_task_obj_init_pass(host_obj):
    def test_func():
        return True

    task = Task(
        task=test_func,
        name="test task",
        hosts=[host_obj, host_obj, host_obj],
        params={"testparam1": "value1"},
        response=Response(),
    )

    assert isinstance(task.task, Callable)
    assert task.task.__name__ == "test_func"
    assert task.name == "test task"
    assert isinstance(task.hosts, list)
    assert isinstance(task.hosts[0], Host)
    assert task.hosts[0].ip == "10.0.0.1"
    assert task.params == {"testparam1": "value1"}
    assert isinstance(task.response, Response)
