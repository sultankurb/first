from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str = None
    ADMIN_ID: int = None
    BOT_TOKEN: str = None


settings = Settings()

async_engine = create_async_engine(url=settings.DATABASE_URL)
async_session_maker = async_sessionmaker(bind=async_engine)
