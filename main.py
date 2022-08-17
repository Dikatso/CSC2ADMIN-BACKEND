from typing import Union
from src.prisma import prisma
from src.apis import apis
from fastapi import FastAPI
from prisma import Prisma
from firebase_admin import credentials, initialize_app, storage

def initialiseFileStorage():
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {'storageBucket': 'cs2admin.appspot.com'})

db = Prisma(auto_register=True)

app = FastAPI()
app.include_router(apis, prefix="/apis")

@app.on_event("startup")
async def startup():
    print("initialising fileStorage...")
    initialiseFileStorage()
    print("connecting to db...")
    await prisma.connect()
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    print("shutting down db...")
    await prisma.disconnect()
    await db.disconnect()

@app.get("/")
def read_root():
    return {"version": "1.0.0"}
