from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Task, Result
import json

nr = InitNornir(config_file="automation/nornir/config.yaml")

def hello_world(task: Task) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} says Hello!"
    )

results = nr.run(task=napalm_get, getters=["interfaces"])
print_result(results)