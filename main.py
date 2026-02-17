import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram import F

from handlers import commands, callbacks, messages

# load_dotenv(dotenv_path="/var/www/vh19393/data/chatgpt-tg-bot/.env")
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

yandex_id = os.getenv('YANDEX_ID')
yandex_key = os.getenv('YANDEX_KEY')
endpoint = os.getenv('ENDPOINT')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher()

dp.include_router(commands.router)
dp.include_router(callbacks.router)
dp.include_router(messages.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())
