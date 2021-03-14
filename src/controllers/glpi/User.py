import requests
import json
from decouple import config

class userController:
    '''
    Controller that holds all process involving users.
    '''
    def __init__(self,app):
        """
        Instantiate the app to control all process involving users
        :param app: The object that has the App instance.
        """
        self.app_token = app.app_token
        self.session_token = app.session_token

    def getClients(self):
        url = config("GLPI_BASEURL") + "/search/User/"
        querystring = {
            "range":"0-1000",
            "order":"ASC",
            "criteria[0][itemtype]":"User",
            "criteria[0][field]":"13",
            "criteria[0][searchtype]":"contains",
            "criteria[0][value]":"Clientes",
            "forcedisplay[0]":["1","2"]
            }
        payload = ""
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        response = requests.request("GET", url, data=payload, params=querystring,headers=headers)
        return response.json()
        
    def getTechs(self):
        url = config("GLPI_BASEURL") + "/search/User/"
        querystring = {
            "range":"0-1000",
            "order":"ASC",
            "criteria[0][itemtype]":"User",
            "criteria[0][field]":"13",
            "criteria[0][searchtype]":"contains",
            "criteria[0][value]":"Área técnica",
            "forcedisplay[0]":"1",
            "forcedisplay[1]":"2",
            "forcedisplay[2]":"9",
            "forcedisplay[3]":"34"
            }
        payload = ""
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        response = requests.request("GET", url, data=payload, params=querystring,headers=headers)
        data = {}
        for tech in response.json().get('data'):
            data[tech['2']]=f"{tech['9']} {tech['34']}"
        return data
