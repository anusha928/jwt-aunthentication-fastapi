import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    
    DB_USER:str = os.getenv('POSTGRES_USER')
    DB_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
    DB_NAME:str = os.getenv('POSTGRES_DB')
    DB_HOST:str = os.getenv('POSTGRES_SERVER')
    DB_PORT:str = os.getenv('POSTGRES_PORT')
    DATABASE_URL :str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

     # JWT 
    JWT_SECRET: str = os.getenv('JWT_SECRET', '83233c855f2e1d6fcca0e745e13e3aa8174ccdc40e0d6be05aa69b5ca25508da')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60)
    
def get_settings()-> Settings:
    return Settings()

# address already in use 
#  sudo lsof -t -i tcp:8000 | xargs kill -9
 