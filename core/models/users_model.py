from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    realname: str
    clubs: list[str] # 속해있는 동아리의 objectId 리스트

