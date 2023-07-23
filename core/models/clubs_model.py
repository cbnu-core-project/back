from pydantic import BaseModel

class Club(BaseModel):
	title: str
	main_content: str
	sub_content: str
	author: str
	user_id: str
	image_urls: list[str]
	activity_tags: list[str]
	tag1: str
	tag2: str
	tag3: str
	classification: int