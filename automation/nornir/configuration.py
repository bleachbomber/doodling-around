from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure, napalm_get
from nornir.core.filter import F
from jinja2 import FileSystemLoader, Environment, PackageLoader, meta
from jinja2.filters import FILTERS
from j2ipaddr import filters
from start import Inventory

#nr = InitNornir(config_file='automation/nornir/config.yaml')
nr = Inventory().return_init()

FILTERS.update(filters.load_all())

loader = FileSystemLoader('.')
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

# Courtesy of https://campusnetworkengineering.com/posts/practical-automation-series-part-2/
def generate_config_and_push(task, part):
    """Render unique device configuration and push to device"""
    rendered_config = task.run(task=template_file, 
                               template=f'{part + "-" + task.host.platform + ".j2"}', 
                               path='automation/nornir/templates/',
                               jinja_env=env).result
    configure_devices = task.run(task=napalm_configure, 
                                 dry_run=False, 
                                 configuration=rendered_config)
    
def get_current_config(task):
    current_config = task.run(task=napalm_get,
                               getters=['config'],
                               retrieve='all')
    
# To fix sections without duplicate code 
# Maybe work on config replace (makes config clean?!)
#results = nr.run(task=generate_config_and_push, part='defaults')
#print_result(results)
#results = nr.run(task=generate_config_and_push, part='ospf')
#print_result(results)
#results = nr.filter(F(groups__contains='core_routing') & F(platform='iosxr')).run(task=generate_config_and_push, part='defaults')
#print_result(results)
results = nr.filter(F(groups__contains='core_routing')).run(task=generate_config_and_push, part='bgp')
print_result(results)