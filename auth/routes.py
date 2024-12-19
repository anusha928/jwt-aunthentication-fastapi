from fastapi import APIRouter, status,Depends
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from auth.services import login_user_account,get_new_access_token

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"],
    responses = {404: {"description": "Not Found"}},
)

# refresh_router = APIRouter(
#     prefix = "/auth",
#     tags = ["Auth"],
#     responses = {404: {"description": "Not Found"}},
# )


@router.post('/token',status_code=status.HTTP_201_CREATED)
def login_user(data:OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    access_token = login_user_account(data=data,db=db)
    payload =  {
                "access_token":access_token.access_token,
                "refresh_token":access_token.refresh_token,
                "token_type": "Bearer"
                 }
    return JSONResponse(content = payload)


@router.get('/refresh',status_code=status.HTTP_200_OK) 
def refresh_token(token:str,  db: Session = Depends(get_db)):
   
    new_access_token = get_new_access_token(refresh_token = token ,db = db)
    payload =  {
                "access_token":new_access_token,
                "token_type": "Bearer"
                 }
    return JSONResponse(content=payload)
    
    


 
