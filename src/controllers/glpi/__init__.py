import os,platform
import json
from decouple import config

from .Session import sessionController
from .Tickets import ticketController

class glpi:
    """
    Instantiate the app object
    """
    def __init__(self):
        self.app_token = config("GLPI_APPTOKEN")
        self.session = sessionController(self.app_token)
        self.session_token = self.session.session_token
        self.tickets = ticketController(self)
        

    def start(self):
        self.app_token = config("GLPI_APPTOKEN")
        self.session_token = self.getToken()

    def getToken(self):
        token = sessionController(self.app_token).createSession()
        return token