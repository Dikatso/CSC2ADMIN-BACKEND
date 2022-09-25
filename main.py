from src.apis import apis
from fastapi import FastAPI
from prisma import Prisma
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from src.utils.email import send_summary_email, configure_enquiries_data
from src.utils.firebase import initialise_file_storage

""" connect to prisma engine """
db = Prisma(auto_register=True)
prisma = Prisma()

""" initialise fastAPI app and attach routes """
app = FastAPI()
app.include_router(apis, prefix="/apis")

""" allow only origins of this link to make API requests """
origins = [
    "http://localhost:3000"
]

""" configure cors middleware for origin"""
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
    initialise_file_storage()
    print("connected successfully ✅")
    print("connecting to prisma...💠")
    await prisma.connect()
    print("connected successfully ✅")
    print("connecting to db...📙")
    await db.connect()
    print("connected successfully ✅")
    print("server initialised & ready to serve 🚀")

@app.on_event("startup")
@repeat_every(seconds=86400)  # 24 hours
async def send_summary_emails() -> None:
    dataList = await configure_enquiries_data()
    await send_summary_email(dataList[0], dataList[1], dataList[2], True)

@app.on_event("shutdown")
async def shutdown():
    print("shutting down db...")
    await prisma.disconnect()
    await db.disconnect()

@app.get("/")
def read_root():
    return {"version": "1.0.0"}
