import requests
import logging
from aiogram import Bot, Dispatcher, executor, types
from tele_bot_api import *
from dotenv import load_dotenv
import os


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get('BOT_API'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm Nakki's echo bot.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)