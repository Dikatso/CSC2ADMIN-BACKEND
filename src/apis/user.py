from fastapi import APIRouter
from prisma.models import User

router = APIRouter()

@router.get("/user/")
async def read_user():
    return {"user1" : "Botshelo"}

@router.get("/users/")
async def read_users():
    users = await User.prisma().find_many()
    return users

@router.post("/user/")
async def create_user():
    user = await User.prisma().create(
        data={
            "name": "bob1",
            "email": "bob1@bob.com",
            "password": "bob1"
        }
    )

    print(user)
