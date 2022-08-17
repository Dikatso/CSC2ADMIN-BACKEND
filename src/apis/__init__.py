from fastapi import APIRouter
from src.apis.auth import router as authRouter
from src.apis.enquiry import router as enquiryRouter
from src.apis.file import router as fileRouter

apis = APIRouter()
apis.include_router(authRouter)
apis.include_router(enquiryRouter)
apis.include_router(fileRouter)
__all__ = ["apis"]