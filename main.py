from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from fastapi import  status,Depends
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from typing import Generator
from users.schemas import CreateUserRequest
from sqlalchemy.orm import Session
from users.services import create_user_account



app = FastAPI(debug=True)

env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

engine = create_engine(
    "postgresql://postgres:Anusha@localhost:5432/fastapi",
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user",status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db : Session = Depends(get_db) ):
     await create_user_account(data=data, db=db)
     payload = {"message":"User created successfully"}
     return JSONResponse(content=payload)

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})