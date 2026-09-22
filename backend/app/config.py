from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=f"{BASE_DIR}/.env", extra="ignore")

    APP_NAME: str = "PackSmart"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'packsmart.db'}"
    ADMIN_TOKEN: str = "packsmart-admin-change-me"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"


settings = Settings()
