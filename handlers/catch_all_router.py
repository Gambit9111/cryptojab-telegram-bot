from aiogram import Router
from aiogram.types import Message

router = Router(name="catch-all-router")

@router.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.answer("Please /start the bot to use it")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")