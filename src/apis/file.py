import io, os
from typing import List
from fastapi import APIRouter, Depends
from src.prisma import prisma
from src.utils.auth import JWTBearer, decodeJWT
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from prisma.models import Enquiry, User
from src.file.fileStorage import upload_file
from firebase_admin import storage
import shutil

router = APIRouter()

@router.post("/file/{enquiryId}", tags=["file"])
async def create_file(enquiryId: str, fileUpload: UploadFile = File(...)):
    fileName = fileUpload.filename

    # save file to local disk
    with open(fileName, "wb") as buffer:
        shutil.copyfileobj(fileUpload.file, buffer)
    
    # upload file from local disk
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    os.remove(fileName) # remove file from local disk

    # allow public access of file
    blob.make_public()

    fileUrl = blob.public_url
    print("file url: ", fileUrl)

    updatedEnquiry = await Enquiry.prisma().update(
        where={
            "id": enquiryId,
        },
        data={
            "attatchmentLink": fileUrl,
        }
    )
    return updatedEnquiry