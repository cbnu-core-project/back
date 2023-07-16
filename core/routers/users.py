from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from config.database import collection_user
from schemas.users_schema import users_serializer
from models.users_model import User
from pydantic import BaseModel

from utils.token import oauth2_schema


router = APIRouter(
	tags=["users"]
)



@router.get("/api/user/info/{email}", description="email(id) 에 맞는 유저의 정보 리턴")
def get_user(email: str):
	user = users_serializer(collection_user.find({"email": email}))[0]
	return user

@router.get("/api/user/info", description="로그인 된 사용자의 정보 가져오기")
def get_user(token: str = Depends(oauth2_schema)):
	# user = verify_token(token)
	return { "_id": user["_id"],"username": user["username"], "realname": user["realname"], "clubs": user["clubs"]}


# 현재 유저가 속한 동아리 리스트 가져오기
@router.get("/api/user/clubs")
def get_user_clubs(token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	clubs = user.get("clubs")

	return clubs

class UserClubs(BaseModel):
	clubs: list[str]


# 유저 동아리 리스트 수정하기 ( 받아온 리스트로 대체 )
@router.put("/api/user/clubs", description="유저 동아리 리스트 수정하기 (보낸 리스트로 전부 대체)")
def update_user_clubs(clubs: UserClubs, token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	clubs_list = dict(clubs).get("clubs")
	collection_user.update_one({"_id": ObjectId(user["_id"])}, {"$set": {"clubs": clubs_list}})
	return "update"

# 유저 동아리 리스트에 동아리 1개 추가하기
@router.post("/api/user/club/push/{objid}", description="유저 동아리 리스트에 동아리 1개 추가")
def push_user_club(objid: str, token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	collection_user.update_one({"_id": ObjectId(user["_id"])}, {"$push": {"clubs": objid}})

	return "push"

class RefreshToken(BaseModel):
	refresh_token: str

@router.post("/api/refresh")
def refresh(token: RefreshToken):
	refresh_token = dict(token).get("refresh_token")
	payload = verify_refresh_token_and_create_access_token(refresh_token)

	new_access_token = payload.get("access_token")
	return new_access_token
