import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

from app.handlers import register_handlers_file
from app.handlers import register_handlers_common
from app.handlers import register_handlers_brands


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Запускает бота'),
        BotCommand(command='/cancel', description='Отменяет действие')
    ]
    await bot.set_my_commands(commands)


async def main():
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

    # PROXY_URL = 'http://proxy.server:3128'
    bot = Bot(token=os.environ.get('BOT_API'), parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp)
    register_handlers_file(dp)
    register_handlers_brands(dp)
    
    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())