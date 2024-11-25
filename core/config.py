# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from urllib.parse import quote_plus
# from pydantic_settings import BaseSettings

# env_path = Path(".")/".env"
# load_dotenv(dotenv_path=env_path)

# class Settings(BaseSettings):
    
#     DB_USER:str = os.getenv('POSTGRES_USER')
#     DB_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
#     DB_NAME:str = os.getenv('POSTGRES_DB')
#     DB_HOST:str = os.getenv('POSTGRES_SERVER')
#     DB_PORT:str = os.getenv('POSTGRES_PORT')
#     DATABASE_URL :str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    
# def get_settings()-> Settings:
#     return Settings
 