from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Task, Result
#from nornir.core.plugins.inventory import TransformFunctionRegister
#from transforming_inventory_data.helpers import update_credentials
import getpass

#TransformFunctionRegister.register('update_credentials', update_credentials)

class Inventory():
    def __init__(self):
        self.nr = InitNornir(config_file="automation/nornir/config.yaml")
        self.set_credentials()

    def return_init(self):
        return self.nr

    #def adapt_host_data(self, host, username, password):
    #    host.

    def get_username(self):
        username = input("Username: ")
        return username
    
    def get_password(self):
        password = getpass.getpass()
        return password
    
    def get_platforms(self):
        platforms = set()
        uniques = []
        for host in self.nr.inventory.hosts:
            platforms.add(self.nr.inventory.hosts[host].dict()['platform'])
        for unique in (list(platforms)):
            uniques.append(unique)
        return uniques

    def set_credentials(self):
        x = y = 0
        for platform in self.get_platforms():
            print(x)
            x += 1
            
            print(f'{"Enter credentials for " + platform + " ... "}')
            username = self.get_username()
            password = self.get_password()
            for key in self.nr.filter(F(platform=f'{platform}')).inventory.hosts.keys():
                print(key)
                
                self.nr.inventory.hosts[key].username = username
                self.nr.inventory.hosts[key].password = password


inv = Inventory()
