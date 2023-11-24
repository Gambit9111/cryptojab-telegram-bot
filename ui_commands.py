from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    """
    Sets bot commands in UI
    :param bot: Bot instance
    """
    commands = [
        BotCommand(command="start", description="Start the bot to purchase subscription to VIP channel"),
        BotCommand(command="join", description="Get the invite link to VIP channel after your payment has been confirmed"),
        BotCommand(command="status", description="Check the status of your subscription"),
        BotCommand(command="cancel", description="Cancel current action"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )