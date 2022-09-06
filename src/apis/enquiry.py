from typing import List
from fastapi import APIRouter, Depends
from src.prisma import prisma
from src.utils.auth import JWTBearer, decodeJWT
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from prisma.models import Enquiry, User

router = APIRouter()

class CreateEnquiryDto(BaseModel):
    userId: str
    type: str  = None
    title: str = None               
    courseCode: str = None                    
    enquiryMessage: str = None      
    extensionDuration: str = None   
    attatchmentLink: str = None     
    assignmentNo: str = None        
    testNo: str = None 

class UpdateEnquiryDto(BaseModel):
    enquiryReplyMessage: str = None
    extensionDuration: str = None
    attatchmentLink: str = None
    assignmentNo: str = None
    status: str = None

@router.post("/enquiry/", tags=["enquiry"])
async def create_enquiry(createEnquiryDto: CreateEnquiryDto):
    createdEnquiry = await Enquiry.prisma().create(
        data={
            "status": "Recieved",
            "type": createEnquiryDto.type,
            "extensionDuration": createEnquiryDto.extensionDuration,
            "testNo": createEnquiryDto.testNo,
            "courseCode": createEnquiryDto.courseCode,
            "userId": createEnquiryDto.userId,
            "title": createEnquiryDto.title,
        },
    )
    return createdEnquiry

@router.get("/enquiry/{enquiryId}", tags=["enquiry"])
async def get_enquiry(enquiryId: str):
    enquiry = await Enquiry.prisma().find_first(
        where={
            "id": enquiryId
        }
    )
    return enquiry

@router.get("/enquiries", tags=["enquiry"])
async def find_all_enquiries():
    enquiry = await Enquiry.prisma().find_many()
    return enquiry

@router.get("/enquiries/{userId}", tags=["enquiry"])
async def find_enquiry_by_user(userId: str):
    enquries = await Enquiry.prisma().find_many(
        where={
            "userId": userId
        }
    )
    return enquries

@router.put("/enquiry/{enquiryId}", tags=["enquiry"])
async def update_enquiry(enquiryId: str, updateEnquiryDto: UpdateEnquiryDto):
    updatedEnquiry = await Enquiry.prisma().update(
        where={
            "id": enquiryId
        },
        data={
            "enquiryReplyMessage": updateEnquiryDto.enquiryReplyMessage,
            "status": updateEnquiryDto.status,
            "extensionDuration": updateEnquiryDto.extensionDuration,
            "attatchmentLink": updateEnquiryDto.attatchmentLink,
            "assignmentNo": updateEnquiryDto.assignmentNo
        }
    )
    return updatedEnquiry

@router.delete("/enquiries", tags=["enquiry"])
async def delete_all():
    await Enquiry.prisma().delete_many()
    return { "message": "ok"}

