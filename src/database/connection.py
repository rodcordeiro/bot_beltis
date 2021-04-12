#########################################################################
#                                                                       #
#                       Grupo Developers                                #
#                                                                       #
#                GNU General Public License v3                          #
#                                                                       #
#########################################################################

from MySQLdb import MySQLError, connect

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
        check_user = self.cursor.execute(f"select * from users u where u.is_admin = true and u.telegram_id = {user.telegram_id}")
        if (check_user == 0):
            return False
        check_user = self.cursor.fetchone()
        user.is_admin = check_user[4]
        user.admin_level = int(check_user[5])
        user.glpi_user = check_user[6]
        user.zabbix_user = check_user[3]
        return user

