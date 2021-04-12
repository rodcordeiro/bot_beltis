#########################################################################
#                                                                       #
#                       Grupo Developers                                #
#                                                                       #
#                GNU General Public License v3                          #
#                                                                       #
#########################################################################


class User:
    def __init__(self, telegram_id, first_name, last_name, username, is_bot, is_admin = False, admin_level = 1, glpi_user = None, zabbix_user = None):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_bot = is_bot
        self.is_admin = is_admin
        self.admin_level = admin_level
        self.glpi_user = glpi_user
        self.zabbix_user = zabbix_user

    def __eq__(self, other):
        return self.telegram_id == other.telegram_id