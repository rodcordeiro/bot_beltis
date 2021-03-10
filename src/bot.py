import logging

from aiogram import types, Bot
from decouple import config

from messages_controller import extract_user_object, extract_message_object, extract_chat_object

bot = Bot(token= config('API_TOKEN'))

class BeltisBot:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.bot = bot
        self.run_bot()

    def run_bot(self):
        @self.dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply("""Beltis TI bot. 
 *AINDA EM PRODUÇÃO*

 Available commands:
  - /help: Provides the command list;
  - /getid: Returns the user id, used to setup the zabbix notifications;
  
""")

        @self.dispatcher.message_handler(commands=['getid'])
        async def return_user_id(message: types.Message):
            msg = extract_user_object(message)
            await message.reply(msg.telegram_id)
        


        @self.dispatcher.message_handler(commands=['teste'])
        async def testMessage(message: types.Message):
            print(message)
            await message.reply(message)
