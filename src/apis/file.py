import io
from typing import List
from fastapi import APIRouter, Depends
from src.prisma import prisma
from src.utils.auth import JWTBearer, decodeJWT
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from prisma.models import Enquiry, User
from src.file.fileStorage import upload_file
from firebase_admin import storage

router = APIRouter()

@router.post("/file/{enquiryId}", tags=["file"])
async def create_file(enquiryId: str, fileUpload: UploadFile = File(...)):
    print("> uploaded file:", fileUpload.filename)

    contents = await fileUpload.read()
    temp_file = io.BytesIO()
    temp_file.write(contents)
    temp_file.seek(0)

    bucket = storage.bucket()
    blob = bucket.blob(fileUpload.filename)
    blob.upload_from_file(temp_file)

    temp_file.close()

    # Opt : if you want to make public access from the URL
    blob.make_public()

    fileUrl = blob.public_url

    updatedEnquiry = await Enquiry.prisma().update(
        where={
            "id": enquiryId,
        },
        data={
            "attatchmentLink": fileUrl,
        }
    )
    return updatedEnquiry