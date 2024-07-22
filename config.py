from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from contextlib import contextmanager
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_psycopg(self):
        # Кодируем части строки подключения
        user = quote(self.DB_USER)
        password = quote(self.DB_PASS)
        host = quote(self.DB_HOST)
        database = quote(self.DB_NAME)
        
        # Формирование DSN
        return f"postgresql+psycopg://{user}:{password}@{host}:{self.DB_PORT}/{database}"
        
    model_config = SettingsConfigDict(env_file=".env")

