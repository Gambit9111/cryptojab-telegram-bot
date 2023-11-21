from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    """
    Sets bot commands in UI
    :param bot: Bot instance
    """
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="join", description="Get a link for the VIP channel"),
        BotCommand(command="help", description="Contact the support team"),
        BotCommand(command="cancel", description="Cancel the current action"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )