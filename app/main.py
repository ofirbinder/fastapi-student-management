from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.routers.api import api_router

API_VERSION = settings.API_VERSION
DATABASE_PATH = settings.DATABASE_PATH
ENV = settings.ENV


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = f"http://{settings.HOST}:{settings.PORT}"
    print("\n" + " ✨ " * 10)
    print("🚀 API RELOADED & READY")
    print(f"🔗 UI: {url}")
    print(f"📖 Docs: {url}/docs")
    print(" ✨ " * 10 + "\n")
    yield


app = FastAPI(
    title="Students API",
    description="API for managing students records and majors.",
    version=f"{API_VERSION}v",
    lifespan=lifespan,
)

setup_exception_handlers(app)


app.include_router(api_router, prefix=f"/api/v{API_VERSION}")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

print(f"Environment state: {ENV}")
