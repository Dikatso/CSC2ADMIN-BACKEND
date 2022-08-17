import datetime
import email
from pickle import TRUE
from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.prisma import prisma
from fastapi.encoders import jsonable_encoder
from prisma.models import User
from fastapi.responses import JSONResponse
from src.utils.auth import (
    encryptPassword,
    signJWT,
    validatePassword,
    decodeJWT,
    JWTBearer
)

router = APIRouter()

class SignUpDto(BaseModel):
    email: str 
    password: str
    name: str
    studentId: str = None
    convenerId: str = None
    taId: str = None
    role: str = None

class SignInDto(BaseModel):
    email: str
    password: str

class SignInResponse(BaseModel):
    token: str
    user: User


@router.get("/auth/sign-in", tags=["auth"])
async def sign_in(signInDto: SignInDto):
    user = await User.prisma().find_first(
        where={
            "email": signInDto.email
        }
    )

    validated = validatePassword(signInDto.password, user.password)
    del user.password

    if validated:
        token = signJWT(user.id)
        return SignInResponse(token=token, user=user)

    return None

@router.get("/auth/user", tags=["auth"])
async def get_current_user(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)

    if "userId" in decoded:
        userId = decoded["userId"]
        return await prisma.user.find_unique(where={"id": userId})
    return None

@router.post("/auth/sign-up", tags=["auth"])
async def sign_up(signUpDto: SignUpDto):
    encryptePassword = encryptPassword(signUpDto.password)

    userCreated = await User.prisma().create(
        data={
            "name": signUpDto.name,
            "email": signUpDto.email,
            "password": encryptePassword,
            "taId": signUpDto.taId,
            "studentId": signUpDto.studentId,
            "convenerId": signUpDto.convenerId,
            "role": signUpDto.role
        }
    )
    return userCreated

@router.post("/auth/users", tags=["auth"])
async def find_all():
    users = await User.prisma().find_many()
    return users

@router.delete("/auth/", tags=["auth"])
async def delete_all():
    await User.prisma().delete_many()
    return { "message": "ok"}
