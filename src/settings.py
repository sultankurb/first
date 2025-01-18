from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")
    BOT_TOKEN: str
    DATABASE_URL: str
    ADMIN_ID: int
    ADMIN_USERNAME: str
    ADMIN_2_ID: int


settings = Settings()

async_engine = create_async_engine(url=settings.DATABASE_URL)
async_session_maker = async_sessionmaker(bind=async_engine)
