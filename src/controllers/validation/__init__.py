import datetime
import base64

from database.connection import Database
from messages_controller import extract_user_object, extract_message_object, extract_chat_object

class validation:
    def __init__(self,app):
        self.app = app
    
    def encode(self,data):
        message = data
        message_bytes = message.encode('ascii')
        encodedToken = base64.b64encode(message_bytes)
        token = encodedToken.decode('ascii')
        return token
    

    def running_proccess(self, user_id, chat_id,message):
        process = self.app.database.get_running_proccess(user_id, chat_id)
        if process == False:
            return
        id = process[0]
        status = process[1]
        pdate = process[2]
        processo = process[3]  
        date = datetime.datetime(pdate.year,pdate.month,pdate.day,pdate.hour,pdate.minute,pdate.second)

        if processo == "ticket_create":
            task = self.ticket_creation_process(user_id, chat_id, process,message)
        
        return task


    def ticket_creation_process(self, user_id, chat_id, task = None,message = None):
        if task == None:
            process = self.app.database.get_proccess_stage(user_id, chat_id, "ticket_create")
        else:
            process = task
        
        id = process[0]
        status = process[1]
        pdate = process[2]
        date = datetime.datetime(pdate.year,pdate.month,pdate.day,pdate.hour,pdate.minute,pdate.second)
        
        today = datetime.datetime.now()
        maxdate=datetime.datetime(today.year,today.month,today.day - 1,today.hour,today.minute,today.second)
        
        if pdate < maxdate:
            self.app.database.update_proccess_stage(id, "completed",1)
            process_id = self.app.database.create_proccess_stage(user_id, chat_id, "ticket_create")
            self.app.database.create_ticket_task(process_id[0])
            self.app.database.update_proccess_stage(id, "stage",1)
            return "Por favor, informe o título para a criação do chamado."

        if status == 0:
            self.app.database.create_ticket_task(id)
            self.app.database.update_proccess_stage(id, "stage",1)
            return "Por favor, informe o título para a criação do chamado."
    
        if status == 1:
            self.app.database.update_ticket_data(id,"title",message.text)
            self.app.database.update_proccess_stage(id, "stage",2)
            return "Por favor, informe a descrição do chamado."

        if status == 2:
            self.app.database.update_proccess_stage(id, "completed",1)
            self.app.database.update_ticket_data(id,"description",message.text)
            ticket = self.app.database.get_ticket_data(id)
            title = ticket[0]
            description = ticket[1]
            self.app.database.delete_ticket_data(id)
            user = self.app.database.get_user(message)
            ticket_id = self.app.glpi.create_ticket(title,description,user)
            if ticket_id:
                return f"Chamado aberto sob ID #{ticket_id} e pode ser acompanhado atráves deste [Link](http://glpi.beltis.com.br/glpi/front/ticket.form.php?id={ticket_id}). A equipe foi notificada e entrará em contato em breve."
            return "Não foi possível abrir o chamado no momento, por favor tente novamente mais tarde."

    def glpi_registration_process(self, user_id, chat_id, task = None,message = None):
        if task == None:
            process = self.app.database.get_proccess_stage(user_id, chat_id, "glpi_registration")
        else:
            process = task
        
        id = process[0]
        status = process[1]
        pdate = process[2]
        date = datetime.datetime(pdate.year,pdate.month,pdate.day,pdate.hour,pdate.minute,pdate.second)
        
        today = datetime.datetime.now()
        maxdate=datetime.datetime(today.year,today.month,today.day - 1,today.hour,today.minute,today.second)
        
        if pdate < maxdate:
            self.app.database.update_proccess_stage(id, "completed",1)
            process_id = self.app.database.create_proccess_stage(user_id, chat_id, "glpi_registration")
            self.app.database.register_glpi_task(process_id[0])
            self.app.database.update_proccess_stage(id, "stage",1)
            return "Por favor, informe seu usuário do GLPI"

        if status == 0:
            self.app.database.register_glpi_task(id)
            self.app.database.update_proccess_stage(id, "stage",1)
            return "Por favor, informe seu usuário do GLPI"
    
        if status == 1:
            self.app.database.update_glpiRegistration_data(id,"user",message.text)
            self.app.database.update_proccess_stage(id, "stage",2)
            return "Por favor, informe sua senha"

        if status == 2:
            self.app.database.update_proccess_stage(id, "completed",1)
            glpi_user = self.app.database.get_glpiRegistration_data(id)
            token = self.encode(f"{glpi_user}:{message.text}")
            self.app.database.register_glpi_user(user_id,token)
            self.app.database.delete_glpiRegistration_data(id)
            return "*Cadastrado!*/n Agora você poderá abrir usar mais funcionalidades do GLPI, como abrir chamados."





