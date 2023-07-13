from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from schemas.schedules_schema import schedules_serializer
from config.database import collection_schedule
from models.schedules_model import Schedule
from utils.token import oauth2_schema, verify_token, verify_schedule_authority

router = APIRouter(
    tags=["schedules"]
)

@router.get('/api/user/schedule')
def get_user_schedule(token: str = Depends(oauth2_schema)):
    user = verify_token(token)
    # 토큰과 권한이 유효하면 밑에 실행
    clubs = user.get('clubs')

    # 검색 조건 설정
    query = {"$or": [{"club_objid": club} for club in clubs]}

    # 검색하기
    results = schedules_serializer(collection_schedule.find(query))

    return results

@router.post('/api/user/schedule')
def create_user_schedule(schedule: Schedule, token: str = Depends(oauth2_schema)):
    schedule = dict(schedule)
    user = verify_schedule_authority(club_objid=schedule.get("club_objid"), token=token)
    collection_schedule.insert_one(dict(schedule))
    return "success"

# 받아온 schedule 데이터로 전부 대체
@router.put('/api/user/schedule')
def update_user_schedule(schedule: Schedule, token: str = Depends(oauth2_schema)):
    schedule = dict(schedule)
    user = verify_schedule_authority(schedule.get("club_objid"), token)
    collection_schedule.update_one({"_id": ObjectId(schedule.get("_id"))}, schedule)

@router.delete('/api/user/schedule/{objid}')
def delete_user_schedule(schedule_objid: str, token: str = Depends((oauth2_schema))):
    try:
        schedule = schedules_serializer(collection_schedule.find({"_id": ObjectId(schedule_objid)}))
        club_objid = schedule[0].get("club_objid")
    except:
        raise HTTPException(status_code=401, detail="유효하지 않은 objid")

    # 권한 및 토큰 검증
    user = verify_schedule_authority(club_objid=club_objid, token=token)
    collection_schedule.delete_one({"_id": ObjectId(schedule_objid)})
    return "delete success"



