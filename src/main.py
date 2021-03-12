import logging
from decouple import config

from aiogram import Dispatcher, executor, types
from bot import BeltisBot, bot

async def warn_startup(startup):
    await bot.send_message(1021953062,"Bot startado")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(bot)
    main = BeltisBot(dp)
    executor.start_polling(dp, skip_updates=True,on_startup=warn_startup)