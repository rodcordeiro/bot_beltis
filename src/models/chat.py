#########################################################################
#                                                                       #
#                       Grupo Developers                                #
#                                                                       #
#                GNU General Public License v3                          #
#                                                                       #
#########################################################################


class Chat:
    def __init__(self, chat_id, chat_type, title=None):
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.title = title

    def __eq__(self, other):
        return self.chat_id == other.chat_id