from typing import Union
from src.prisma import prisma
from src.apis import apis
from fastapi import FastAPI
from prisma import Prisma
from firebase_admin import credentials, initialize_app, storage
from fastapi.middleware.cors import CORSMiddleware

def initialiseFileStorage():
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {'storageBucket': 'cs2admin.appspot.com'})

db = Prisma(auto_register=True)

app = FastAPI()
app.include_router(apis, prefix="/apis")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print("initialising server...🏗")
    print("connecting to firebase storage...🔥")
    print("connected successfully ✅")
    initialiseFileStorage()
    print("connecting to prisma...💠")
    print("connected successfully ✅")
    await prisma.connect()
    print("connecting to db...📙")
    print("connected successfully ✅")
    await db.connect()
    print("server initialised & ready to serve 🚀")

@app.on_event("shutdown")
async def shutdown():
    print("shutting down db...")
    await prisma.disconnect()
    await db.disconnect()

@app.get("/")
def read_root():
    return {"version": "1.0.0"}
