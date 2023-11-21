from sqlalchemy import create_engine, inspect

from db.base import Base
from db.models import User

from config import DB_URL


engine = create_engine(DB_URL, echo=True)
Base.metadata.drop_all(engine)  #uncomment this line to wipe the database

exist = inspect(engine).has_table("user")
if not exist:
    Base.metadata.create_all(engine)
