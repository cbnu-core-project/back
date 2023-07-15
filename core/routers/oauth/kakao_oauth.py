import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.database import collection_user
from enum import Enum
import json
from models.users_model import User, SocialEnum
from schemas.others_schema import others_serializer

REST_API_KEY = "40d478c8d7447b20143b402959fd7ed8";
REDIRECT_URI = "http://localhost:3000";
KAKAO_USERINFO_URL = 'https://kapi.kakao.com/v2/user/me'

# + code 랑 같이 쓰여야 됨
KAKAO_GET_TOKEN_URL = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code="

router = APIRouter(
	tags=["kakao_oauth"]
)

class Code(BaseModel):
	code: str

def get_user_info(access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	response = requests.get(KAKAO_USERINFO_URL, headers=headers,
							# params={"property_keys": json.dumps(["kakao_account.email"])}
	)

	if not response.ok:
		raise HTTPException(
			status_code=401,
			detail="잘못 된 access_token",
			headers={"WWW-Authenticate": "Bearer"},
		)

	return response.json()

def user_register(user):
	# 이미 가입된 이메일이면
	email = user.get('kakao_account').get('email')
	if(others_serializer(collection_user.find({"email": email}))):
		return False

	# 가입되지 않은 이메일이면
	collection_user.insert_one({"email": user.get('kakao_account').get('email'),
								"realname": "",
								"nickname": user.get('kakao_account').get('profile').get('nickname'),
								"profile_image_url": user.get('kakao_account').get('profile').get('profile_image_url'),
								"social": SocialEnum.kakao,
								"clubs": [],
								"refresh_token": "",
								"authority": 4,
								"major": "",
								"student_number": "",
								"phone_number": "",
								})
	return True

@router.post("/oauth/kakao/callback")
def kakao_oauth(code: Code):
	code = dict(code).get('code')
	headers = { "Content-type": "application/x-www-form-urlencoded;charset=utf-8" }
	response = requests.post(KAKAO_GET_TOKEN_URL + code, headers=headers).json()

	access_token = response.get('access_token')
	refresh_token = response.get('refresh_token')
	user_info = get_user_info(access_token)

	email = user_info.get('kakao_account').get('email')
	is_email_valid = user_info.get('kakao_account').get('is_email_valid')
	is_email_verified = user_info.get('kakao_account').get('is_email_verified')

	if (not(is_email_valid) or not(is_email_verified)):
		raise HTTPException(
			status_code=401,
			detail="유효하지 않거나 인증되지 않은 이메일",
			headers={"WWW-Authenticate": "Bearer"},
		)

	if (user_register(user_info)):
		print("회원가입 완료")

	return { "access_token": access_token, "refresh_token": refresh_token }


