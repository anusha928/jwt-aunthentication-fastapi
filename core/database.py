# from core.config import get_settings
# from sqlalchemy.orm import sessionmaker,declarative_base
# from sqlalchemy import create_engine
# from typing import Generator
# # from sqlalchemy_utils import database_exists, create_database


# settings = get_settings()
# # print("Environment Variables Loaded:")
# # print(f"DB_PASSWORD: {settings.DB_PASSWORD}")
# # print(f"DB_NAME: {settings.DB_NAME}")
# # print(f"DB_HOST: {settings.DB_HOST}")
# # print(f"DB_PORT: {settings.DB_PORT}")

# engine = create_engine(
#     settings.DATABASE_URL,
#     pool_pre_ping=True,
#     pool_recycle=300,
#     pool_size=5,
#     max_overflow=0
# )
# print("database urlllllllllllllllllllllllllllllllllllllllllllll- {DATABASE_URL}")

# # if not database_exists(engine.url):
# #     create_database(engine.url)

# SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
# print("db Connected successfully!")

# Base = declarative_base()

# def get_db() -> Generator:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
    