import logging
import sys

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import (
                    TELEGRAM_BOT_TOKEN, 
                    TELEGRAM_WEBHOOK_URL, 
                    TELEGRAM_WEBHOOK_SECRET,
                    TELEGRAM_ADMIN_ID, 
                    DB_URL,
                    WEB_SERVER_HOST,
                    WEB_SERVER_PORT
                    )
from handlers import main_router, new_member_router, catch_all_router, cancel_sub_router, admin_router
from middlewares import DbSessionMiddleware
from ui_commands import set_ui_commands


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(TELEGRAM_WEBHOOK_URL, drop_pending_updates=True, secret_token=TELEGRAM_WEBHOOK_SECRET)
    bot_info = await bot.get_me()
    webhook_info = await bot.get_webhook_info()
    # Set bot commands in UI
    await set_ui_commands(bot)
    await bot.send_message(chat_id=TELEGRAM_ADMIN_ID, text="Bot is starting")
    print("**************__Initializing the bot__**************\n")
    print("**************__Bot info__**************\n")
    print(bot_info)
    print("\n")
    print(webhook_info)

async def on_shutdown(bot: Bot) -> None:
    print("**************__Bot is shutting down__**************\n")
    await bot.session.close()


def main() -> None:

    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)

    engine = create_async_engine(DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")

    # Setup dispatcher
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_router(main_router.router)
    dp.include_router(admin_router.router)
    dp.include_router(new_member_router.router)
    dp.include_router(cancel_sub_router.router)
    dp.include_router(catch_all_router.router)
    
    try:
        aiohttp_logger = logging.getLogger("aiohttp.access")
        aiohttp_logger.setLevel(logging.CRITICAL)
        
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
    
        app = web.Application()

        # Create an instance of request handler,
        # aiogram has few implementations for different cases of usage
        # In this example we use SimpleRequestHandler which is designed to handle simple cases
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=TELEGRAM_WEBHOOK_SECRET,
        )
        webhook_requests_handler.register(app, path="/")
    
        # Mount dispatcher startup and shutdown hooks to aiohttp application
        setup_application(app, dp, bot=bot)

        # And finally start webserver
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    
    except Exception as e:
        logging.exception(e)
        sys.exit(1)
    


if __name__ == "__main__":
    main()