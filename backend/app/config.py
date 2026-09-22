from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "PackSmart"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'packsmart.db'}"

    class Config:
        env_file = f"{BASE_DIR}/.env"
        extra = "ignore"


settings = Settings()
