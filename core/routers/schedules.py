from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .users import verify_token
from schemas.schedules_schema import schedules_serializer
from config.database import collection_schedule
from models.schedules_model import Schedule

router = APIRouter(
    tags=["schedules"]
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login")

@router.get('/api/user/schedule')
def get_user_schedule(token: str = Depends(oauth2_schema)):
    user = verify_token(token).get("user")
    # 토큰이 유효하면, 밑에 실행
    clubs = user[0].get('clubs')

    # 검색 조건 설정
    query = {"$or": [{"club_objid": club} for club in clubs]}

    # 검색하기
    results = schedules_serializer(collection_schedule.find(query))

    return results

@router.post('/api/user/schedule')
def post_user_schedule(schedule: Schedule, token: str = Depends(oauth2_schema)):
    collection_schedule.insert_one(dict(schedule))

    return "success"