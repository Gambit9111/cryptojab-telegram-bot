from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Users
from aiogram import Bot

from datetime import datetime, timedelta

from config import TELEGRAM_PREMIUM_CHANNEL_ID, TELEGRAM_ADMIN_ID


async def user_exists(telegram_id: int, session: AsyncSession, Users: Users) -> bool:
    """
    Description:
        query the database to check if the user with given telegram_id exists
    Params: 
        telegram_id (int): telegram_id of the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        Boolean: False if user does not exist, True if user exists
    """
    try:
        sql = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(sql)
        user = result.scalars().first()
        
        if user is None:
            return False
        
        if user is not None:
            return True
    except Exception as e:
        print("function user_exists ERROR", e)


async def generate_invite_link(telegram_id: int, session: AsyncSession, Users: Users, bot: Bot) -> str:
    """
    Description:
        generate an invite link for the user with given telegram_id
    Params: 
        telegram_id (int): telegram_id of the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        invite_link (str): invite link for the user
    """
    try:
        sql = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(sql)
        user: Users = result.scalars().first()
        
        if user is None or user.generated_invite_link is True:
            return "You have already generated an invite link!"
        
        if user is not None:
            
            await bot.unban_chat_member(chat_id=TELEGRAM_PREMIUM_CHANNEL_ID, user_id=telegram_id)
            # generate new invite link
            link_expire_date = datetime.now() + timedelta(minutes=60)
            invite = await bot.create_chat_invite_link(chat_id=TELEGRAM_PREMIUM_CHANNEL_ID, name=str(telegram_id), member_limit=1, expire_date=link_expire_date)
            invite_link = invite.invite_link
            
            # update the database
            user.generated_invite_link = True
            await session.commit()
            
            return invite_link
        
    except Exception as e:
        print("function generate_invite_link ERROR", e)

