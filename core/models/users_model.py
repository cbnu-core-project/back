from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    realname: str
    nickname: str
    clubs: list[str] # 속해있는 동아리의 objectId 리스트
    refresh_token: str
    authority: int
    major: str
    student_number: str
    phone_number: str



