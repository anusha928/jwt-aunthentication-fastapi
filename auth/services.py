from fastapi.exceptions import  HTTPException
from datetime import datetime, timedelta, timezone
from typing import  Union
from core.security import verify_password
from users.models import UserModel
import jwt
from core.config import get_settings
from auth.response import TokenResponse

settings = get_settings()


# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "83233c855f2e1d6fcca0e745e13e3aa8174ccdc40e0d6be05aa69b5ca25508da"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


def login_user_account(data,db):
    user =  authenticate_user(data=data,db=db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.first_name},expires_delta=access_token_expires)
    return TokenResponse(access_token=access_token,expires_in=access_token_expires.seconds)


def authenticate_user(data,db):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email is not registered",headers={"WWW-Authenticate":"Bearer"})
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Login Credentials",headers={"WWW-Authenticate":"Bearer"})
    return user



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data):
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

