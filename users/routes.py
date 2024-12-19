from fastapi import APIRouter, status,Depends,Request
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account
from fastapi.responses import JSONResponse
from users.services import oauth2_scheme
from users.response import UserResponse;
from starlette.authentication import UnauthenticatedUser
from fastapi import HTTPException, status

router = APIRouter(
    prefix = "/user",
    tags = ["Users"],
    responses = {404: {"description": "Not Found"}},
)

user_router = APIRouter(
    prefix = "/user",
    tags = ["Users"],
    responses = {404: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post('',status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db : Session = Depends(get_db) ):
     await create_user_account(data=data, db=db)
     payload = {"message":"User created successfully"}
     return JSONResponse(content=payload)
    
@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(request: Request):
    return request.user

