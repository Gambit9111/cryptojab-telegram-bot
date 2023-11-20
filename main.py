import logging
import sys

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import TELEGRAM_BOT_TOKEN, DB_URL
from handlers import commands
from middlewares import DbSessionMiddleware
from ui_commands import set_ui_commands



async def main():
    engine = create_async_engine(DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
    
    # Setup dispatcher and bind routers to it
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    
    # Register handlers
    dp.include_router(commands.router)
    
    # Set bot commands in UI
    await set_ui_commands(bot)
    # run bot
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())