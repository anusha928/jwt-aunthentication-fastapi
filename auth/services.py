from fastapi.exceptions import  HTTPException
from datetime import datetime, timedelta, timezone
from typing import  Union
from core.security import verify_password
from users.models import UserModel,RefreshTokenModel
import jwt
from core.config import get_settings
from auth.response import TokenResponse
from starlette.authentication import AuthCredentials, UnauthenticatedUser



settings = get_settings()


# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "83233c855f2e1d6fcca0e745e13e3aa8174ccdc40e0d6be05aa69b5ca25508da"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


def login_user_account(data,db):
    user =  authenticate_user(data=data,db=db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires =  timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAY)
    access_token = create_access_token(data={"sub": user.first_name},expires_delta=access_token_expires)
    print(f"Access token : {access_token}")
    refresh_token = create_refresh_token(data={"sub": user.first_name},expires_delta=refresh_token_expires)
    store_refresh_token(data, db,refresh_token,refresh_token_expires)
    return TokenResponse(access_token=access_token,expires_in=access_token_expires.seconds,refresh_token=refresh_token)

def store_refresh_token(data, db,refresh_token,expires_at:Union[timedelta, None] = None):
    expire = datetime.now(timezone.utc) +expires_at
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    existing_token = db.query(RefreshTokenModel).filter(RefreshTokenModel.user_id == user.id).first()
    if existing_token:
        # Update the existing token
        existing_token.refresh_token = refresh_token
        existing_token.expires_at = expire
        existing_token.is_revoked = False
        print(f"refresh token updated successfully : refreshtoken :{existing_token.refresh_token}")


    else:
       refresh_token = RefreshTokenModel(
        user_id = user.id,
        refresh_token = refresh_token,
        expires_at= expire
    )
       db.add(refresh_token)
       print(f"refresh token saved successfully : refreshtoken :{refresh_token.refresh_token}")

    db.commit()
    

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

def create_refresh_token(data:dict,expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.REFRESH_SECRET, algorithm=settings.REFRESH_ALGORITHM)

def validate_refresh_token(token: str):
    """
    Validates and decodes the refresh token.
    """
    try:
        payload = jwt.decode(token, settings.REFRESH_SECRET, algorithms=[settings.REFRESH_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
def get_new_access_token(refresh_token: str, db):
    # Validate the refresh token
    payload = validate_refresh_token(refresh_token)
    user_identifier = payload.get("sub")
    if not user_identifier:
        raise HTTPException(status_code=400, detail="Invalid refresh token payload")

    # Fetch the user from the database
    user = db.query(UserModel).filter(UserModel.first_name == user_identifier).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the refresh token exists and matches
    existing_token = db.query(RefreshTokenModel).filter(RefreshTokenModel.user_id == user.id).first()
    if not existing_token or existing_token.refresh_token != refresh_token:
        raise HTTPException(status_code=400, detail="Invalid or expired refresh token")

    # Generate a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = jwt.encode(
        {"sub": user.first_name, "exp": (datetime.now(timezone.utc) + access_token_expires)},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return new_access_token
