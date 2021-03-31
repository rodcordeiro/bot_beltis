import requests
import json
from decouple import config

from .Session import sessionController
from .Tickets import ticketController
from .User import userController

class glpi:
    """
    Instantiate the app object
    """
    def __init__(self):
        self.app_token = config("GLPI_APPTOKEN")
        self.session = sessionController(self.app_token)
        self.session_token = self.session.session_token
        self.users = userController(self)
        self.tickets = ticketController(self)

    def getTicket(self,ticket_id):
        ticket = self.tickets.getTicket(ticket_id)
        if ticket:
            return ticket
        else:
            self.session = sessionController(self.app_token)
            self.session_token = self.session.session_token
            self.getTicket(ticket_id)
        