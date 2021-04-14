#########################################################################
#                                                                       #
#                       Grupo Developers                                #
#                                                                       #
#                GNU General Public License v3                          #
#                                                                       #
#########################################################################

from MySQLdb import MySQLError, connect
import datetime
from decouple import config

from messages_controller import extract_message_object, extract_chat_object, extract_user_object


class Database():
    def __init__(self):
        self.connect()


    def connect(self):
        self.db = connect(host=config("DB_HOST"), db=config("DB_NAME"),
                            user=config("DB_USER"),passwd=config("DB_PASSWORD"))
        self.cursor = self.db.cursor()
        self.ping = self.db.ping(True)

    def is_admin(self, user_id):
        self.ping
        check_user = self.cursor.execute(f"select admin_level from users u where u.is_admin = true and u.telegram_id = {user_id}")
        if (check_user == 0):
            return False
        return self.cursor.fetchone()

    def get_user(self, message):
        self.ping
        user = extract_user_object(message)
        check_user = self.cursor.execute(f"select * from users u where u.telegram_id = {user.telegram_id}")
        if (check_user == 0):
            return False
        check_user = self.cursor.fetchone()
        user.is_admin = bool(check_user[4])
        user.admin_level = check_user[6] if check_user[6] != None else 0
        user.glpi_user = check_user[5]
        user.zabbix_user = check_user[3]
        return user
    
    def get_running_proccess(self,user_id, chat_id):
        response = self.cursor.execute(f"select id,stage,datetime,proccess from status_control sc where sc.user_id='{user_id}' and sc.chat_id = '{chat_id}' and sc.completed = 'false';")
        if response == 0:
            return False
        else:
            response = self.cursor.fetchone()
        return response
    

    def get_proccess_stage(self,user_id, chat_id, process):
        query = f"select id,stage,datetime from status_control sc where sc.user_id='{user_id}' and sc.chat_id = '{chat_id}' and sc.proccess like '{process}' and sc.completed = 'false';"
        response = self.cursor.execute(f"select id,stage,datetime from status_control sc where sc.user_id='{user_id}' and sc.chat_id = '{chat_id}' and sc.proccess like '{process}' and sc.completed = 'false';")
        if response == 0:
            response = self.create_proccess_stage(user_id, chat_id, process)
        else:
            response = self.cursor.fetchone()
        return response
    
    def create_proccess_stage(self,user_id, chat_id, process):
        date = datetime.datetime.now()
        response = self.cursor.execute(f"insert into status_control(user_id,chat_id,proccess,datetime) values('{user_id}', '{chat_id}', '{process}', '{date}');")
        id = self.cursor.execute(f"select id,stage,datetime from status_control sc where sc.user_id='{user_id}' and sc.chat_id = '{chat_id}' and sc.proccess like '{process}' and sc.completed = 'false' order by id desc limit 1;")
        id = self.cursor.fetchone()
        self.db.commit()
        return id
    
    def update_proccess_stage(self,process_id, column,value):
        self.cursor.execute(f"update status_control set {column} = '{value}' where id = '{process_id}'")        
        self.db.commit()

    def create_ticket_task(self,process_id):
        self.cursor.execute(f"insert into ticket_creation(proccess_id) value ('{process_id}');")
        self.db.commit()
    
    def update_ticket_data(self,process_id, column,value):
        self.cursor.execute(f"update ticket_creation set {column} = '{value}' where proccess_id = '{process_id}'")        
        self.db.commit()

    def get_ticket_data(self,process_id):
        self.cursor.execute(f"select title,description from ticket_creation t where t.proccess_id = '{process_id}';")
        return self.cursor.fetchone()

    def delete_ticket_data(self,process_id):
        self.cursor.execute(f"delete from  ticket_creation where proccess_id = '{process_id}'")        
        self.db.commit()