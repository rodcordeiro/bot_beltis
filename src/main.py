import logging

from aiogram import Dispatcher, executor, types
from bot import BeltisBot, bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(bot)
    main = BeltisBot(dp)
    executor.start_polling(dp, skip_updates=True)