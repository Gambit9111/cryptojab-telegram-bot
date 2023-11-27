from aiogram import Router
from aiogram.types import Message

from data import (
    CATCH_ALL_MESSAGE,
    CATCH_ALL_WRONG_TYPE_MESSAGE
)

router = Router(name="catch-all-router")

@router.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.answer(CATCH_ALL_MESSAGE)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer(CATCH_ALL_WRONG_TYPE_MESSAGE)