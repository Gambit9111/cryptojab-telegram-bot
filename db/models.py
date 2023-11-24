from sqlalchemy import Column, Integer, BigInteger, Enum, DateTime, Boolean
from datetime import datetime

from .base import Base

class Users(Base):
    __tablename__ = 'users'
    
    _id = Column("id", Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    payment_method = Column(Enum('stripe', 'coinbase', name="payment_method"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    generated_invite_link = Column(Boolean, default=False, nullable=False)
    
    
    def __init__(self, telegram_id, payment_method, valid_until):
        self.telegram_id = telegram_id
        self.payment_method = payment_method
        self.valid_until = valid_until

    def __repr__(self):
       return '<User %r>' % self.telegram_id