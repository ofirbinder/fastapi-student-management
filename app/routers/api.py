from fastapi import APIRouter

from app.routers import student_router

api_router = APIRouter()
api_router.include_router(student_router.router, prefix="/students", tags=["Students"])
