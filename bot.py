import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from decouple import config

from app.handlers.main import main_handler


async def main():
    bot = Bot(token=config('BOT_TOKEN'),
              default=DefaultBotProperties(
              parse_mode="HTML"))

    await bot.delete_webhook()
    dp = Dispatcher()

    dp.include_router(main_handler)

    await dp.start_polling(bot,
                           polling_timeout=100)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
        print("Bot start")
    except KeyboardInterrupt:
        print('Bot stop')
    except Exception as e:
        print(e)

