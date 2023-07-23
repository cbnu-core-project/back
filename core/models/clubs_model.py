from pydantic import BaseModel

class Club(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	image_url: str
	activity_tags: list[str]
	tag1: str
	tag2: str
	tag3: str
	classification: int