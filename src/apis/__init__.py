from fastapi import APIRouter
from src.apis.user import router as userRouter

apis = APIRouter()
apis.include_router(userRouter)
__all__ = ["apis"]