def club_serializer(club) -> dict:
	return {
		"_id": club["_id"],
		"title": club["title"],
		"content": club["content"],
		"author": club["author"],
		"user_id": club["user_id"],
		"image_url": club["image_url"],
		"tag1": club["tag1"],
		"tag2": club["tag2"],
		"tag3": club["tag3"],
		"classification": club["classification"]
	}

def clubs_serializer(clubs) -> list:
	return [club_serializer(club) for club in clubs]