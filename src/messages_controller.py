#########################################################################
#                                                                       #
#                       Grupo Developers                                #
#                                                                       #
#                GNU General Public License v3                          #
#                                                                       #
#########################################################################

from models.message import Message
from models.chat import Chat
from models.user import User

def extract_message_object(telegram_message):
    return Message(
        message_id=telegram_message.message_id,
        text=telegram_message.text,
        date=telegram_message.date,
        chat_id=telegram_message.chat.id,
        author_id=telegram_message['from'].id,
        reply_message_id=telegram_message.reply_to_message if hasattr(
            telegram_message, 'reply_to_message') else ""
    )


def extract_chat_object(telegram_message):
    return Chat(
        chat_id=telegram_message.chat.id,
        chat_type=telegram_message.chat.type,
        title=telegram_message.chat.title if hasattr(
            telegram_message.chat, 'title') else ""
    )


def extract_user_object(telegram_message):
    return User(
        telegram_id=telegram_message['from'].id,
        first_name=telegram_message['from'].first_name,
        last_name=telegram_message['from'].last_name or '',
        username=telegram_message['from'].username or '',
        is_bot=telegram_message['from'].is_bot
    )