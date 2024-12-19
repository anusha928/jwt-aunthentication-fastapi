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
    JWT_SECRET: str = os.getenv('JWT_SECRET', '88cc41eb5898b6c7ca090a895e8f8f382e643431c6c4f2519c7f0da413284726')
    REFRESH_SECRET: str = os.getenv('REFRESH_SECRET', '88cc41eb5898b6c7ca090a895e8f8f382e643431c6c4f2519c7f0da413284726')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    REFRESH_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60)
    REFRESH_TOKEN_EXPIRE_DAY: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAY', 7)

    
def get_settings()-> Settings:
    return Settings()

# address already in use 
#  sudo lsof -t -i tcp:8000 | xargs kill -9
 