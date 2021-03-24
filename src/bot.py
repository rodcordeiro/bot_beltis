import logging
import os
from aiogram import types, Bot
from decouple import config

from messages_controller import extract_user_object, extract_message_object, extract_chat_object
from controllers.glpi import glpi
from controllers.zabbix import zabbix

bot = Bot(token= config('API_TOKEN'))

class BeltisBot:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.bot_name = "Beltis TI bot"
        self.bot_description = "*AINDA EM PRODUÇÃO*"
        self.bot = bot
        self.version = "1"
        self.glpi = glpi()
        self.zabbix = zabbix()
        self.run_bot()

    def run_bot(self):
        print(os.path.realpath('./version'))
        @self.dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply(f"""{self.bot_name}. 
 {self.bot_description}

 Available commands:
  - /help: Retorna a lista de comandos habilitados;
  - /getid: Retorna seu id de usuário, esta informação é utilizada pelo suporte para habilitar notificações;
  - /ticket ID: Retorna as informações sobre um ticket específico;
  - /validate: Validates bot information and session connections
""")

        @self.dispatcher.message_handler(commands=['getid'])
        async def return_user_id(message: types.Message):
            msg = extract_user_object(message)
            await message.reply(msg.telegram_id)

        @self.dispatcher.message_handler(commands=['ticket'])
        async def ticket_handler(message: types.Message):
            if (len(message.text) > 7):
                ticket_id = message.text.split(' ')[1]
                ticket_status =  self.glpi.getTicket(ticket_id)
                await message.reply(ticket_status)
            else:
                await message.reply("Criar ticket")

        @self.dispatcher.message_handler(commands=['zhost'])
        async def zabbix_host(message: types.Message):
            if (len(message.text) <= 6):
                response = self.zabbix.getHosts()
                await message.reply(response)
            else:
                await message.reply("Criar ticket")

        @self.dispatcher.message_handler(commands=['teste'])
        async def testMessage(message: types.Message):
            print(message)
            await message.reply(message)
    
        @self.dispatcher.message_handler(commands=['validate'])
        async def validate_glpi_api(message: types.Message):
            await message.reply(f">- BOT:\n    {self.bot_name} {self.version}\n\n>- GLPI:\n    App-Token: {self.glpi.app_token}\n    Session-Token: {self.glpi.session_token}\n\n>- Zabbix:\n    User: {self.zabbix.session['alias']}\n    Session: {self.zabbix.session['sessionid']}")
    
        @self.dispatcher.message_handler()
        async def messages_helper(message: types.Message):
            await message.reply("Oi, ainda não estou configurado para ser um chatbot completo, mas se estiver precisando de ajuda use /help que eu te mostro o que já posso fazer!")
    