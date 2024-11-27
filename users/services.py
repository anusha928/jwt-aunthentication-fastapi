from users.models import UserModel
from fastapi.exceptions import  HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import jwt
from pydantic import BaseModel



# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "83233c855f2e1d6fcca0e745e13e3aa8174ccdc40e0d6be05aa69b5ca25508da"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def create_user_account(data,db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="This email is already registered")
    
    hashed_pd = get_password_hash(data.password)
    new_user = UserModel(
        first_name = data.first_name,
        last_name = data.last_name,
        email = data.email,
        password = hashed_pd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

    
async def login_user_account(data,db):
    user = authenticate_user(data=data,db=db)
    if not user:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED: Incorrect user name or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.first_name},expires_delta=access_token_expires)
    return access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(data,db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if not user:
        return False
    if not verify_password(data.password, user.password):
        return False
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

