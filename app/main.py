from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions_backup import setup_exception_handlers
from app.routers.api import api_router

API_VERSION = settings.API_VERSION
DATABASE_PATH = settings.DATABASE_PATH
ENV = settings.ENV

app = FastAPI(title="Students API")
setup_exception_handlers(app)


app.include_router(api_router, prefix=f"/api/v{API_VERSION}")

print(f"Environment state: {ENV}")
