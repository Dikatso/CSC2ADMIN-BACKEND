from typing import Union
from src.prisma import prisma
from src.apis import apis
from fastapi import FastAPI
from prisma import Prisma

db = Prisma(auto_register=True)

app = FastAPI()
app.include_router(apis, prefix="/apis")

@app.on_event("startup")
async def startup():
    print("connecting to db...")
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    print("shutting down db...")
    await db.disconnect()

@app.get("/")
def read_root():
    return {"version": "1.0.0"}
