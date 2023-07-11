from config.database import collection_club
from schemas.clubs_schema import clubs_serializer
from schemas.users_schema import users_serializer

def club_image_url_conversion():
    # collection_club.update_many({}, {"$rename": {"image_url": "image_urls"}})
    clubs = clubs_serializer(collection_club.find())
    for club in clubs:
        image = club.get("image_urls")
        collection_club.update_one({"_id": club.get("_id")}, {'$set':{"image_urls": [image]}})



if __name__ == "__main__":
    pass
