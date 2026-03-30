from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str 
    access_token_expires_minutes: int 
    refresh_token_expires_days: int 
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()

class Base(DeclarativeBase):
    pass 

engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False}
    )

LocalSession = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

