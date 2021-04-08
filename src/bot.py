import logging
import os
from aiogram import types, Bot
from decouple import config

from messages_controller import extract_user_object, extract_message_object, extract_chat_object
from controllers.glpi import glpi
from controllers.zabbix import zabbix
from database.connection import Database

bot = Bot(token= config('API_TOKEN'),parse_mode="markdown")

class BeltisBot:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.bot_name = "Beltis TI bot"
        self.bot_description = "*AINDA EM PRODUÇÃO*"
        self.bot = bot
        self.get_version()
        self.glpi = glpi()
        self.zabbix = zabbix()
        self.database = Database()
        self.run_bot()

    def get_version(self):
        path=os.path.join(os.path.split(os.path.dirname(__file__))[0],'version')
        version=open(path,'r').read()
        self.version=version


    def run_bot(self):
        @self.dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply(f"""*{self.bot_name}.*
 _{self.bot_description}_

 Available commands:
  - /help: Retorna a lista de comandos habilitados;
  - /getid: Retorna seu id de usuário do telegram;
  - /getgroup: Retorna a id do grupo;
""")

#   - /ticket ID: Retorna as informações sobre um ticket específico;
#   - /validate: Validates bot information and session connections

        @self.dispatcher.message_handler(commands=['getid'])
        async def return_user_id(message: types.Message):
            await bot.send_chat_action(message.chat.id,"typing")
            msg = extract_user_object(message)
            await message.reply(msg.telegram_id)
        
        @self.dispatcher.message_handler(commands=['getgroup'])
        async def return_user_id(message: types.Message):
            await bot.send_chat_action(message.chat.id,"typing")
            chat = extract_chat_object(message)
            if chat.chat_type != "group":
                await message.reply("Por favor, execute este comando em um grupo para que a informação possa ser retornada corretamente.")
            else:
                await message.reply(chat.chat_id)

        @self.dispatcher.message_handler(commands=['ticket'])
        async def ticket_handler(message: types.Message):
            if (len(message.text) > 7):
                ticket_id = message.text.split(' ')[1]
                await bot.send_chat_action(message.chat.id,"typing")
                ticket_status =  self.glpi.getTicket(ticket_id)
                await message.reply(ticket_status)
            else:
                await message.reply("Criar ticket")

        @self.dispatcher.message_handler(commands=['zhosts'])
        async def zabbix_hosts(message: types.Message):
            await bot.send_chat_action(message.chat.id,"typing")
            response = self.zabbix.getHosts()
            await message.reply(response)
        
        @self.dispatcher.message_handler(commands=['zhost'])
        async def zabbix_host(message: types.Message):
            await bot.send_chat_action(message.chat.id,"typing")
            response = self.zabbix.getHost()
            await message.reply(response)

        @self.dispatcher.message_handler(commands=['teste'])
        async def testMessage(message: types.Message):
            print(message)
            await message.reply(message)
    
        @self.dispatcher.message_handler(commands=['validate'])
        async def validate_glpi_api(message: types.Message):
            await bot.send_chat_action(message.chat.id,"typing")
            user = self.database.validate_admin_exist(message)
            if user:
                await message.reply(f">- *BOT:*\n    _{self.bot_name}_ `{self.version}`\n\n>- *GLPI:*\n    _App-Token:_ `{self.glpi.app_token}`\n    _Session-Token:_ `{self.glpi.session_token}`\n\n>- *Zabbix:*\n    _User:_ `{self.zabbix.session['alias']}`\n    _Session:_ `{self.zabbix.session['sessionid']}`")
            else:
                await message.reply("Comando não autorizado")
    
        @self.dispatcher.message_handler()
        async def messages_helper(message: types.Message):
            if message.chat.type != "group" and message.entities[0].type == "bot_command":
                await message.reply("Oi, ainda não estou configurado para ser um chatbot completo ou não reconheço este comando, mas se estiver precisando de ajuda use /help que eu te mostro o que já posso fazer!")
            else:
                return