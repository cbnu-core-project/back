from pydantic import BaseModel

# 각종 데이터 모델들을 정의하는 파일
class Club(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	image_url: str
	tag1: str
	tag2: str
	tag3: str
	classification: int