from fastapi import APIRouter
from bson.json_util import loads, dumps
from pydantic import BaseModel
from bson import ObjectId

from config.yurim_database import coll_club_activity_history

router = APIRouter(
    tags=["club_acticity_history"],
    prefix="/api/club_activity_history"
)


@router.get("")
def read_club_activity_history():
    data = loads(dumps(coll_club_activity_history.find()))

    return data


@router.get("/{club_objid}")
def read_club_activity_history(club_objid: str):
    data = loads(dumps(coll_club_activity_history.find({"club_objid": club_objid})))

    return data

class ClubActivityHistory(BaseModel):
    title: str
    year: str
    month: str
    club_objid: str

@router.post("")
def create_club_activity_history(club_activity_history: ClubActivityHistory):
    coll_club_activity_history.insert_one(dict(club_activity_history))
    return "추가 성공"

@router.delete("/{objid}")
def delete_club_activity_history(objid: str):
    coll_club_activity_history.delete_one({"_id": ObjectId(objid)})
    return "삭제 성공"

@router.put("/{objid}")
def update_club_activity_history(objid: str, club_activity_history: ClubActivityHistory):
    coll_club_activity_history.update_one({"_id": ObjectId(objid)}, {"$set": dict(club_activity_history)})
    return "변경"



