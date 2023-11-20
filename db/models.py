from sqlalchemy import Column, BigInteger

from .base import Base

class User(Base):
    __tablename__ = 'user'
    
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)