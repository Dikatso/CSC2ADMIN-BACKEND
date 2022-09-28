from pickle import TRUE
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from prisma.models import User
from src.utils.auth import (
    encryptPassword,
    signJWT,
    validatePassword,
    decodeJWT,
    JWTBearer
)

router= APIRouter()


class SignUpDto(BaseModel):
    email: str
    password: str
    name: str
    uctId: str
    role: str


class SignInDto(BaseModel):
    email: str
    password: str


class SignInResponse(BaseModel):
    token: str
    user: User


def centraliseDto(dto):
    # remove keys that have no data
    centraliseDto = {}
    for value in (dto):
        key = list(value)[0]
        value = list(value)[1]
        if value is not None:
            centraliseDto[str(key)] = str(value)

    return centraliseDto


@router.post("/auth/sign-in", tags=["auth"])
async def sign_in(signInDto: SignInDto):
    user = await User.prisma().find_first(
        where={
            "email": signInDto.email
        }
    )

    if user is None:
        raise HTTPException(status_code=404, detail="User record doesn't exist")
        
    validated = validatePassword(signInDto.password, user.password)

    if validated:
        del user.password, user.createdAt, user.Enquiries, user.updatedAt
        token = signJWT(user)
        return SignInResponse(token=token, user=user)

    raise HTTPException(status_code=404, detail="Incorrect email or password")


@router.get("/auth/user", tags=["auth"])
async def get_current_user(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)

    if "userId" in decoded:
        userId = decoded["userId"]
        return await User.prisma().find_unique(where={"id": userId})

    raise HTTPException(status_code=404, detail="Not authenticated")



@router.post("/auth/sign-up", tags=["auth"])
async def sign_up(signUpDto: SignUpDto):
    encryptePassword = encryptPassword(signUpDto.password)
    signUpDto.password = encryptePassword
    centralisedDto = centraliseDto(signUpDto)

    existingUser = await User.prisma().find_first(
        where={
            "email": signUpDto.email
        },
    )

    if existingUser:
        raise HTTPException(status_code=404, detail="Email already in use")
    
    existingUser = await User.prisma().find_first(
        where={
            "uctId": signUpDto.uctId
        },
    )
    
    if existingUser:
        raise HTTPException(status_code=404, detail="UCT Id already in use")

    createdUser = await User.prisma().create(
        data=centralisedDto,
    )

    return createdUser


@router.get("/auth/users", tags=["auth"])
async def find_all():
    users = await User.prisma().find_many()
    return users


@router.delete("/auth/", tags=["auth"])
async def delete_all():
    await User.prisma().delete_many()
    return {"message": "ok"}
