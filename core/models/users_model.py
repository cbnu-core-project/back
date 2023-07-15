from pydantic import BaseModel
from enum import Enum


class User(BaseModel):
    email: str
    realname: str
    nickname: str
    profile_image_url: str
    social: str
    clubs: list[str] # 속해있는 동아리의 objectId 리스트
    refresh_token: str
    authority: int
    major: str
    student_number: str
    phone_number: str

class SocialEnum(str, Enum):
	kakao = "kakao"
	naver = "naver"
	google = "google"

