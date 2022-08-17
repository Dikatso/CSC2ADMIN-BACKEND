from fastapi import APIRouter
<<<<<<< HEAD
=======
from src.apis.user import router as userRouter
>>>>>>> b9a8076171250f51a3eb1253ed4080fba765f840
from src.apis.auth import router as authRouter
from src.apis.enquiry import router as enquiryRouter
from src.apis.file import router as fileRouter

apis = APIRouter()
<<<<<<< HEAD
=======
apis.include_router(userRouter)
>>>>>>> b9a8076171250f51a3eb1253ed4080fba765f840
apis.include_router(authRouter)
apis.include_router(enquiryRouter)
apis.include_router(fileRouter)
__all__ = ["apis"]