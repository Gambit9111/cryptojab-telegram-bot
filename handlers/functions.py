from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Users
from aiogram import Bot

from datetime import datetime, timedelta, timezone

from config import TELEGRAM_PREMIUM_CHANNEL_ID, TELEGRAM_ADMIN_ID

from .checkout import stripe


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

async def create_new_user(telegram_id: int, sub_duration:int, session: AsyncSession, Users: Users) -> None:
    """
    Description:
        create a new user in the database
    Params: 
        telegram_id (int): telegram_id of the user
        sub_duration (int): subscription duration for the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        None
    """
    try:
        # calculate valid_until date
        valid_until = datetime.now(timezone.utc) + timedelta(days=sub_duration)
        print("valid until-----------------", valid_until)
        # create a new user
        new_user = Users(telegram_id=telegram_id, payment_method='coinbase', subscription_id='null', valid_until=valid_until)
        session.add(new_user)
        await session.commit()
    except Exception as e:
        print("function create_new_user ERROR", e)

async def can_generate_invite_link(telegram_id: int, session: AsyncSession, Users: Users) -> bool:
    """
    Description:
        check if the user with given telegram_id can generate an invite link
    Params: 
        telegram_id (int): telegram_id of the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        Boolean: False if user cannot generate an invite link, True if user can generate an invite link
    """
    try:
        sql = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(sql)
        user: Users = result.scalars().first()
        
        if user is None:
            return False
        
        if user is not None:
            if user.generated_invite_link is True:
                return False
            
            if user.generated_invite_link is False:
                return True
    except Exception as e:
        print("function can_generate_invite_link ERROR", e)


async def generate_invite_link(telegram_id: int, session: AsyncSession, Users: Users, bot: Bot) -> str:
    """
    Description:
        generate an invite link for the user with given telegram_id, send the notification to admin
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
        
        await bot.unban_chat_member(chat_id=TELEGRAM_PREMIUM_CHANNEL_ID, user_id=telegram_id)
        # generate new invite link
        link_expire_date = datetime.now() + timedelta(minutes=60)
        invite = await bot.create_chat_invite_link(chat_id=TELEGRAM_PREMIUM_CHANNEL_ID, name=str(telegram_id), member_limit=1, expire_date=link_expire_date)
        invite_link = invite.invite_link
        
        # update the database
        user.generated_invite_link = True
        await session.commit()
        
        await bot.send_message(chat_id=TELEGRAM_ADMIN_ID, text=f"User with telegram_id {telegram_id} generated an invite link")
        return invite_link
        
    except Exception as e:
        print("function generate_invite_link ERROR", e)


async def get_sub_duration(telegram_id: int, session: AsyncSession, Users: Users) -> datetime:
    """
    Description:
        get the subscription duration for the user with given telegram_id
    Params: 
        telegram_id (int): telegram_id of the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        sub_duration (int): subscription duration for the user
    """
    try:
        sql = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(sql)
        user: Users = result.scalars().first()
        
        # calculate how many days user has left
        sub_duration = user.valid_until - datetime.utcnow()
        return sub_duration.days
        
    except Exception as e:
        print("function get_sub_duration ERROR", e)

async def cancel_subscription(telegram_id: int, session: AsyncSession, Users: Users, bot: Bot) -> None:
    """
    Description:
        cancel users subscription, kick him out of the group and delete from the database, cancel subscription in stripe if the payment method was stripe
    Params: 
        telegram_id (int): telegram_id of the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        None
    """
    try:
        sql = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(sql)
        user: Users = result.scalars().first()
    
        # cancel subscription in stripe
        if user.payment_method == "stripe":
            stripe.Subscription.delete(user.subscription_id)
        
        # delete user from the database
        await session.delete(user)
        await session.commit()
    
    except Exception as e:
        print("function cancel_subscription ERROR", e)


    await bot.unban_chat_member(chat_id=TELEGRAM_PREMIUM_CHANNEL_ID, user_id=telegram_id)
    await bot.send_message(chat_id=TELEGRAM_ADMIN_ID, text=f"User with telegram_id {telegram_id} canceled his subscription")
        

def is_admin(telegram_id: str) -> bool:
    """
    Description:
        check if the user with given telegram_id is admin
    Params: 
        telegram_id (int): telegram_id of the user
    Returns:
        Boolean: False if user is not admin, True if user is admin
    """
    if telegram_id == TELEGRAM_ADMIN_ID:
        return True
    else:
        return False
