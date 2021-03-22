import requests
import json
from decouple import config
import datetime

class ticketController:
    '''
    Instantiate the app to control all process involving tickets
    '''
    def __init__(self,app):
        """
        Instantiate the app to control all process involving tickets
        :param app: The object that has the App instance.
        """
        self.app_token = app.app_token
        self.session_token = app.session_token
        self.techs = app.techs
        self.ticket_status = ["novo", "processando (atríbuido)", "processando (planejado)", "Pendente", "Solucionado", "Fechado"]
        self.ticket_request_type = {
            4: "Direct",
            2: "E-mail",
            1: "Helpdesk",
            6: "Other",
            3: "Phone",
            7: "Whatsapp",
            5: "Written"
        }
        

    def getTicket(self,id):
        """
        Returns the last month tickets, if :id is provided it filters for the user.

        Examples:

        .. code-block:: python

            getTicketsLastMonth(13)

        :param id: ID to be used for filtering the requester of the tickets.
        """

        url = config("GLPI_BASEURL") + "/Ticket/" + id
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        payload = ""
        response = requests.request("GET", url, data=payload,headers=headers)
        if response.status_code == 200:
            ticket = response.json()
            ticket['status'] = self.ticket_status[ticket['status'] - 1]
            ticket['requesttypes_id'] = self.ticket_request_type[ticket['requesttypes_id']]
            ticket['followups'] = self.getTicketFollowups(id)
            try:
                ticket['tech'] = self.techs[ticket['users_id_recipient']]
            except:
                ticket['tech'] = "Analista não encontrado"
            ticket['documents'] = self.getTicketDocuments(id)
            
            ticket_message = f"""---------------------------------
    Ticket ID: {ticket['id']}
    Ticket name: {ticket['name']}
    Ticket description: {ticket['content']}

    Aberto pelo analista: {ticket['tech']}
    Ticket status: {ticket['status']}

---------------------------------
Acompanhamentos:
  """     
            for followup in ticket['followups']:
                ticket_message += f""">{self.techs[followup['users_id']]} em {followup['date']}:
    | {followup['content']}

  """
            ticket_message +="---------------------------------"
            return ticket_message
        return "Ticket não encontrado"
        
    def getTicketFollowups(self,id):
        url = config("GLPI_BASEURL") + "/Ticket/{}/TicketFollowup/".format(id)
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        payload = ""
        response = requests.request("GET", url, data=payload,headers=headers).json()
        return response

    def getTicketDocuments(self,id):
        url = config("GLPI_BASEURL") + "/Ticket/{}/Document_Item/".format(id)
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        payload = ""
        response = requests.request("GET", url, data=payload,headers=headers).json()
        documents = []
        for document in response:
            document['filename'] = self.getDocumentName(document['id'])
            try:
                document['author'] = self.techs[document['users_id']]
            except:
                document['author'] = "Analista não encontrado"
            
            documents.append(document)
        return documents

    def getDocumentName(self,id):
        url = config("GLPI_BASEURL") + "/Document/{}".format(id)
        headers={"Content-Type":"application/json","App-Token":self.app_token,"Session-Token":self.session_token}
        payload = ""
        response = requests.request("GET", url, data=payload,headers=headers).json()
        return response.get('filename')

    def getTicketsLastMonth(self,id=None):
        """
        Returns the last month tickets, if :id is provided it filters for the user.

        Examples:

        .. code-block:: python

            getTicketsLastMonth(13)

        :param id: ID to be used for filtering the requester of the tickets.
        """
        url = config("GLPI_BASEURL") + "/search/Ticket/"
        date = getMonth()
        querystring = {
            "Content-Type":"application/json",
            "app_token":self.app_token,
            "session_token":self.session_token,
            "range":"0-99999",
            "order":"DESC",
            "criteria[0][itemtype]": "Ticket",
            "criteria[0][field]": "15",
            "criteria[0][searchtype]": "morethan",
            "criteria[0][value]": datetime.datetime.strftime(date["init"],"%Y-%m-%d %H:%M:%S"),
            "criteria[1][link]": "AND",
            "criteria[1][itemtype]": "Ticket",
            "criteria[1][field]": "15",
            "criteria[1][searchtype]": "lessthan",
            "criteria[1][value]": datetime.datetime.strftime(date["end"],"%Y-%m-%d %H:%M:%S"),
            "criteria[2][link]": "AND",
            "criteria[2][itemtype]": "Ticket",
            "criteria[2][searchtype]": "equals",
            "criteria[2][value]": id,
            "criteria[2][field]": "4",
            "forcedisplay[0]": "1",
            "forcedisplay[1]": "2",
            "forcedisplay[2]": "12",
            "forcedisplay[3]": "15",
            "forcedisplay[4]": "19",
            "forcedisplay[5]": "3",
            "forcedisplay[6]": "4",
            "forcedisplay[7]": "5",
            "forcedisplay[8]": "7",
            "forcedisplay[9]": "45",
            "forcedisplay[10]": "36",
            "forcedisplay[11]": "9"
            }
        payload = ""
        response = requests.request("GET", url, data=payload, params=querystring)
        return response.json().get("data")

def getMonth():
    date = datetime.date.today()
    if date.month == 1:
        monthInit = 12 
        yearInit = date.year - 1
    else:
        monthInit = date.month - 1
        yearInit = date.year
    init = "{}-{}-{} 00:00:00".format(monthInit, "01",yearInit)
    end = "{}-{}-{} 00:00:00".format(date.month, "01",date.year)
    date = {
        "init":datetime.datetime.strptime(init, "%m-%d-%Y %H:%M:%S").date(),
        "end":datetime.datetime.strptime(end, "%m-%d-%Y %H:%M:%S").date()
        }
    return date