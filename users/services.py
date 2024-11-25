from users.models import UserModel
from fastapi.exceptions import  HTTPException
from passlib.context import CryptContext

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
    
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)