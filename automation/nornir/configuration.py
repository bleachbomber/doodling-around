from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure
from jinja2 import FileSystemLoader, Environment
from jinja2.filters import FILTERS
from j2ipaddr import filters
from start import Inventory

#nr = InitNornir(config_file='automation/nornir/config.yaml')
nr = Inventory().return_init()

FILTERS.update(filters.load_all())

loader = FileSystemLoader('.')
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

# Courtesy of https://campusnetworkengineering.com/posts/practical-automation-series-part-2/
def generate_config_and_push(task):
    """Render unique device configuration and push to device"""
    rendered_config = task.run(task=template_file, 
                               template=f'{"ospf-" + task.host.platform + ".j2"}', 
                               path='automation/nornir/templates/',
                               jinja_env=env).result
    configure_devices = task.run(task=napalm_configure, 
                                 dry_run=True, 
                                 configuration=rendered_config)

results = nr.run(task=generate_config_and_push)
print_result(results)