from pydantic import BaseModel


class User(BaseModel):
    email: str
    realname: str
    nickname: str
    profile_image_url: str
    social: str
    clubs: list[dict] # 속해있는 동아리
    refresh_token: str
    authority: int
    major: str
    student_number: str
    phone_number: str


