from bson import ObjectId
from fastapi import APIRouter
from config.database import collection_notice
from models.notices_model import Notice
from schemas.notices_schema import notice_serializer, notices_serializer

router = APIRouter(
	tags=["notices"]
)

@router.get("/api/notices", description="공지사항 전체 가져오기")
async def read_all_notice():
	notices = notices_serializer(collection_notice.find())

	return notices

@router.get("/api/notices/some/", description="공지사항 skip, limit를 통한 동아리 일부 가져오기\nex) 3번째부터 4개 가져오려면, -> skip=2, limit=4")
async def read_some_club(skip: int, limit: int):
	notices = notices_serializer(collection_notice.find().skip(skip).limit(limit))

	return notices

@router.post("/api/notice", description="공지사항 추가하기")
async def create_notice(notice: Notice):
	_id = collection_notice.nisert_one(dict(notice))
	notice = notices_serializer(collection_notice.find({"_id": _id.inserted_id}))

	return notice

@router.delete("/api/notice/{objid}", description="공지사항 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_notice(objid: str):
	collection_notice.delete_one({"_id": ObjectId(objid)})
	return []