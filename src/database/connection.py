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

    def validate_admin_exist(self, message):
        self.ping
        user = extract_user_object(message)
        check_user = self.cursor.execute(f"select * from users u where u.is_admin = true and u.telegram_id = {user.telegram_id}")
        if (check_user == 0):
            return False
        return True

    def chat_exists(self, chat_id):
        self.ping
        check_chat = self.cursor.execute(f"SELECT * FROM chats WHERE chat_id={chat_id}")
        if (check_chat == 0):
            return False
        return self.cursor.fetchone()
