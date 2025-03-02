import asyncio
import logging.config
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from logging_setting import logging_config
from config import load_config, Config
from handlers import router
from init_pole import pole
from middleware import RootMiddleware
from dialogs import start_dialog


logging.config.dictConfig(logging_config)
ligger = logging.getLogger(__name__)

config: Config = load_config()


async def main():
    bot = Bot(config.tg_bot.TOKEN)
    dp = Dispatcher()
    dp['pole'] = pole
    dp.include_router(router)
    #  dp.update.middleware(RootMiddleware())
    dp.include_router(start_dialog)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
