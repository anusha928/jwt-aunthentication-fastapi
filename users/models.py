from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    