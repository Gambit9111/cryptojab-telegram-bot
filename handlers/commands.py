from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

from .functions import user_exists, create_user

router = Router(name="commands-router")

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    
    
    await message.answer("WELCOME MESSAGE", reply_markup=ReplyKeyboardRemove())
    
    if await user_exists(message.from_user.id, session, User):
        
        await message.answer(
            text="Hello, you are a old user!",
            reply_markup=ReplyKeyboardRemove())
    
    else:
        
        await message.answer(
            text="Hello, you are a new user! we will register you in our database",
            reply_markup=ReplyKeyboardRemove())
        
        await create_user(message.from_user.id, session, User)