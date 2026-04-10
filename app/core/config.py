import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path, override=True)


class Settings:
    API_VERSION: str = os.getenv("API_VERSION", "1")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "app/db/students.json")
    ENV: str = os.getenv("APP_ENV", "development")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))


settings = Settings()
