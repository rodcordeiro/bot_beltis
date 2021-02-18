import logging

from aiogram import types, Bot
from decouple import config

from messages_controller import extract_user_object

bot = Bot(token= config('API_TOKEN'))

class BeltisBot:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.bot = bot
        self.run_bot()

    def run_bot(self):
        @self.dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply("Beltis TI bot. \n\n AINDA EM PRODUÇÃO")

        @self.dispatcher.message_handler(commands=['teste'])
        async def testMessage(message: types.Message):
            print(message)
            msg = extract_user_object(message)
            await message.reply(msg.telegram_id)
