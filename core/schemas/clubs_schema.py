def club_serializer(club) -> dict:
	return {
		"_id": club["_id"],
		"title": club["title"],
		"content": club["content"],
		"user_objid": club["user_objid"],
		"image_urls": club["image_urls"],
		"nickname": club["nickname"],
		"tag1": club["tag1"],
		"tag2": club["tag2"],
		"tag3": club["tag3"],
		"classification": club["classification"]
	}

def clubs_serializer(clubs) -> list:
	return [club_serializer(club) for club in clubs]