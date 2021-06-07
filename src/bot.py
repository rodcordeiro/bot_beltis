import logging
import os
from aiogram import types, Bot
from decouple import config

from messages_controller import extract_user_object, extract_message_object, extract_chat_object
from controllers.glpi import glpi
from controllers.zabbix import zabbix
from controllers.validation import validation
from database.connection import Database

bot = Bot(token= config('API_TOKEN'),parse_mode="markdown")

class BeltisBot:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.bot_name = "Beltis TI bot"
        self.bot_description = "*AINDA EM PRODUÇÃO*"
        self.bot = bot
        self.get_version()
        self.connections = {
            "glpi": False,
            "zabbix": False,
            "database": False
        }
        self.connect()
        self.validation = validation(self)
        self.run_bot()
        
        
        
    def get_version(self):
        path=os.path.join(os.path.split(os.path.dirname(__file__))[0],'version')
        version=open(path,'r').read()
        self.version=version

    def connect(self):
        try:
            self.glpi = glpi()
            self.connections['glpi'] = True
        except:
            pass
        try:
            self.zabbix = zabbix()
            self.connections['zabbix'] = True
        except:
            pass
        try:
            self.database = Database()
            self.connections['database'] = True
        except:
            pass

    def run_bot(self):
        @self.dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            user = self.database.get_user(message)
            help_message=f"""*{self.bot_name}.*
 _{self.bot_description}_

 Available commands:
  - /help: Retorna a lista de comandos habilitados;
  - /getid: Retorna seu id de usuário do telegram;
  - /getgroup: Retorna a id do grupo;
"""
            if user:
                help_message+="""   - /ticket ID: Retorna as informações sobre um ticket específico;
   - /validate: Validates bot information and session connections"""

            await message.reply(help_message)


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
            await bot.send_chat_action(message.chat.id,"typing")
            if (len(message.text) > 7):
                ticket_id = message.text.split(' ')[1]
                ticket_status =  self.glpi.getTicket(ticket_id)
                await message.reply(ticket_status)
            else:
                chat = extract_chat_object(message)
                user = extract_user_object(message)
                response = self.validation.ticket_creation_process(user.telegram_id,chat.chat_id)
                await message.reply(response)

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

        @self.dispatcher.message_handler(commands=['info'])
        async def testMessage(message: types.Message):
            user = self.database.get_user(message)
            print(user,message)
            await message.reply(message)
        
        @dp.message_handler(commands=['teste'])
        async def teste(message: types.Message):
            await bot.send_poll(1016560417,'Qual a boa?',['Supimpa','Tranquilo','Só desgraça','Irineu'],disable_notification=None,reply_to_message_id='962')

    
        @self.dispatcher.message_handler(commands=['validate'])
        async def validate_glpi_api(message: types.Message):
            await bot.send_chat_action(message.chat.id,"typing")
            if self.connections['database'] == False:
                await message.reply("Bot em manutenção. Por favor, contate os administradores.")
                return
            user = self.database.get_user(message)
            if user.is_admin == False:
                await message.reply("Comando não autorizado")
            else:
                msg = f">- *BOT:*\n    _{self.bot_name}_  `{self.version}`"
                msg += f"\n\n>- *Database:*\n    Status: `{self.connections['database']}`"
                msg += f"\n\n>- *GLPI:*\n    Status: `{self.connections['glpi']}`"
                if user.admin_level >= 3:
                    msg += f"\n    _App-Token:_ `{self.glpi.app_token}`\n    _Session-Token:_ `{self.glpi.session_token}`"
                msg += f"\n\n>- *Zabbix:*\n    Status: `{self.connections['zabbix']}`\n"
                if user.admin_level >= 3:
                    msg += f"    _User:_ `{self.zabbix.session['alias']}`\n    _Session:_ `{self.zabbix.session['sessionid']}`"
                await message.reply(msg)
                
    
        @self.dispatcher.message_handler()
        async def messages_helper(message: types.Message):
            if message.chat.type != "group":
                chat = extract_chat_object(message)
                user = extract_user_object(message)
                response = self.validation.running_proccess(user.telegram_id,chat.chat_id,message)
                if response:
                    await message.reply(response)
            else:
                return