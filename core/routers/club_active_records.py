from fastapi import APIRouter
from schemas.others_schema import others_serializer
from config.database import collection_club_active_record

router = APIRouter(
    tags=["club_active_records"]
)


@router.get("/api/club_active_records", description="동아리 활동기록 전체(동아리구분없이) 가져오기")
def read_club_active_records_all():
    club_active_records = others_serializer(collection_club_active_record.find())
    return club_active_records

@router.get("/apu/club_active_records/{club_objid}")
def read_club_active_records_all(club_objid: str):
    club_active_records = others_serializer(collection_club_active_record.find({"club_objid": club_objid}))
    return club_active_records