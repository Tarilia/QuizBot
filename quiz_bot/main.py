import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import asyncio
import logging

from quiz_bot.bot_handlers import register_handlers
from quiz_bot.database import create_table

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def main():
    await create_table()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
