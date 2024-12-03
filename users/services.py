from users.models import UserModel
from fastapi.exceptions import  HTTPException
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from core.security import get_password_hash
from jose import jwt, JWTError
from core.database import get_db
from fastapi import Depends
from core.config import get_settings
from fastapi.security import OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
settings = get_settings()

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

def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db = None):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None

    user_name = payload.get('sub', None)
    if not user_name:
        return None

    if not db:
        db = next(get_db())

    user = db.query(UserModel).filter(UserModel.first_name == user_name).first()
    return user
    
class JWTAuth:
    
    async def authenticate(self, conn):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        if 'authorization' not in conn.headers:
            return guest
        
        token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
        if not token:
            return guest
        
        user = get_current_user(token=token)
        
        if not user:
            return guest
        
        return AuthCredentials('authenticated'), user

    




