import datetime

from database.connection import Database
from messages_controller import extract_user_object, extract_message_object, extract_chat_object

class validation:
    def __init__(self,app):
        self.database = Database()
        self.app = app

    def running_proccess(self, user_id, chat_id,message):
        process = self.database.get_running_proccess(user_id, chat_id)
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
            process = self.database.get_proccess_stage(user_id, chat_id, "ticket_create")
        else:
            process = task
        
        id = process[0]
        status = process[1]
        pdate = process[2]
        date = datetime.datetime(pdate.year,pdate.month,pdate.day,pdate.hour,pdate.minute,pdate.second)
        
        today = datetime.datetime.now()
        maxdate=datetime.datetime(today.year,today.month,today.day - 1,today.hour,today.minute,today.second)
        
        if pdate < maxdate:
            self.database.update_proccess_stage(id, "completed",1)
            process_id = self.database.create_proccess_stage(user_id, chat_id, "ticket_create")
            self.database.create_ticket_task(process_id[0])
            self.database.update_proccess_stage(id, "stage",1)
            return "Por favor, informe o título para a criação do chamado."

        if status == 0:
            self.database.create_ticket_task(id)
            self.database.update_proccess_stage(id, "stage",1)
            return "Por favor, informe o título para a criação do chamado."
    
        if status == 1:
            self.database.update_ticket_data(id,"title",message.text)
            self.database.update_proccess_stage(id, "stage",2)
            return "Por favor, informe a descrição do chamado."

        if status == 2:
            self.database.update_proccess_stage(id, "completed",1)
            self.database.update_ticket_data(id,"description",message.text)
            ticket = self.database.get_ticket_data(id)
            title = ticket[0]
            description = ticket[1]
            self.database.delete_ticket_data(id)
            user = self.database.get_user(message)
            ticket_id = self.app.glpi.create_ticket(title,description,user)
            if ticket_id:
                return f"Chamado aberto sob ID #{ticket_id} e pode ser acompanhado atráves deste [Link](http://glpi.beltis.com.br/glpi/front/ticket.form.php?id={ticket_id}). A equipe foi notificada e entrará em contato em breve."
            return "Não foi possível abrir o chamado no momento, por favor tente novamente mais tarde."



