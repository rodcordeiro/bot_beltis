import requests
import json
from decouple import config

class sessionController:
    def __init__(self,app_token):
        self.app_token = app_token
        self.session_token = ''
        self.createSession()
    
    def createSession(self):
        url = config("GLPI_BASEURL") + "/initSession"
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Authorization":"user_token {}".format(config("GLPI_USERTOKEN"))}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            token = response.json().get("session_token")
            self.session_token = token
        else:
            return False
    
    def killSession(self):
        url = config("GLPI_BASEURL") + "/killSession"
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        response = requests.get(url, headers=headers)
        return response.status_code
    
    def getProfiles(self):
        url = config("GLPI_BASEURL") + "/getMyProfiles"
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        response = requests.get(url, headers=headers)
        return response.json()
