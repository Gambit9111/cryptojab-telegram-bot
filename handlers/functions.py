from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


async def user_exists(telegram_id: int, session: AsyncSession, User: User) -> bool:
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
    
    sql = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(sql)
    user = result.scalars().first()
    
    if user is None:
        return False
    
    if user is not None:
        return True


async def create_user(telegram_id: int, session: AsyncSession, User: User) -> None:
    """
    Description:
        creates new user with the given telegram_id
    Params: 
        telegram_id (int): telegram_id of the user
        session (AsyncSession): AsyncSession object
        User (User): User model
    Returns:
        None
    """

    await session.merge(User(telegram_id=telegram_id))
    await session.commit()