import requests
import json
from decouple import config
from pyzabbix import ZabbixAPI

class zabbix:
    """
    Instantiate the app object
    """
    def __init__(self):
        self.zabbix = ZabbixAPI(config('ZABBIX_HOST'))
        self.zabbix.login(user=config('ZABBIX_USER'),password=config('ZABBIX_PWD'))
        self.session = self.zabbix.check_authentication()
        self.hosts = self.zabbix.host.get({"output":"extend"})

    def getHosts(self):
        response = []
        for host in self.hosts:
            response.append(host['name'])
        return response
    
    def getHost(self):
        host = self.hosts[0]
        host['items'] = self.zabbix.item.get({"output":"extend","select_triggers":"extend","hostids":[host['hostid']]})
        print(host['hostid'])
        return host