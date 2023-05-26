import certifi
import pydantic
import pymongo
from bson import ObjectId

################################################################
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['core_data']

collection_club = db['club']
collection_promotion = db['promotion']
collection_notice = db['notice']
collection_user = db['user']
################################################################