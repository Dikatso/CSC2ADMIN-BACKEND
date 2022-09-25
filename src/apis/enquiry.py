from fastapi import APIRouter
from pydantic import BaseModel
from prisma.models import Enquiry

router = APIRouter()

class CreateEnquiryDto(BaseModel):
    userId: str
    type: str  = None
    title: str = None               
    courseCode: str = None                    
    extensionDuration: str = None   
    attatchmentLink: str = None     
    assignmentNo: str = None        
    testNo: str = None 
    messageFromStudent: str = None
    messageFromConvener: str = None

class UpdateEnquiryDto(BaseModel):
    extensionDuration: str = None
    assignmentNo: str = None
    status: str = None
    attatchmentLink: str = None
    messageFromStudent: str = None
    messageFromConvener: str = None

def centraliseDto(dto):
    # remove keys that have no data
    centraliseDto = {}
    for value in (dto):
        key = list(value)[0]
        value = list(value)[1]
        if value is not None:
            centraliseDto[str(key)] = str(value)

    return centraliseDto

@router.post("/enquiry/", tags=["enquiry"])
async def create_enquiry(createEnquiryDto: CreateEnquiryDto):
    centralisedDto = centraliseDto(createEnquiryDto)

    createdEnquiry = await Enquiry.prisma().create(
        data=centralisedDto,
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
    enquiry = await Enquiry.prisma().find_many(
        include={
            "user": True
        }
    )
    return enquiry

@router.get("/enquiries/{userId}", tags=["enquiry"])
async def find_enquiry_by_user(userId: str):
    enquries = await Enquiry.prisma().find_many(
        where={
            "userId": userId
        },
        include={
            "user": True
        }
    )
    return enquries

@router.put("/enquiry/{enquiryId}", tags=["enquiry"])
async def update_enquiry(enquiryId: str, updateEnquiryDto: UpdateEnquiryDto):
    centralisedDto = centraliseDto(updateEnquiryDto)
    
    enquiry = await Enquiry.prisma().find_first(
        where={
            "id": enquiryId
        },
    )

    if enquiry:
        updatedEnquiry = await Enquiry.prisma().update(
            where={
                "id": enquiryId
            },
            data=centralisedDto
        )
        return updatedEnquiry
    return None

@router.delete("/enquiry/{enquiryId}", tags=["enquiry"])
async def delete_enquiry(enquiryId: str):
    deletedEnquiry = await Enquiry.prisma().delete(
        where={
            "id": enquiryId
        }
    )
    return deletedEnquiry

@router.delete("/enquiries", tags=["enquiry"])
async def delete_all():
    await Enquiry.prisma().delete_many()
    return { "message": "ok"}

