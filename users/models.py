from sqlalchemy import Boolean, Column, Integer, String, DateTime, func,ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base
from core.database import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    
class RefreshTokenModel(Base):
    __tablename__ = 'refresh_tokens'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    created_at = Column(DateTime,default=func.now())
    expires_at = Column(DateTime(255),index=True, nullable=False)
    is_revoked = Column(Boolean, default=False)
    