from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Task, Result
import json

nr = InitNornir(config_file="automation/nornir/config.yaml")

results = nr.run(task=napalm_get, getters=["interfaces"])
print_result(results)