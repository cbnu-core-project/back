# 동아리 정보를 딕셔너리로 반환 (JSON 형식)
# 하나의 동아리 정보를 처리하는 serializer
# club: 동아리 정보
# return: 동아리 정보 딕셔너리
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

# 동아리 정보를 리스트로 반환
# 여러 동아리 정보를 처리하는 serializer
# clubs: 동아리 정보
# return: 동아리 정보 리스트
def clubs_serializer(clubs) -> list:
	return [club_serializer(club) for club in clubs]

# 나머지 serializer들도 위와 같은 방식으로 작성됨
# serializer는 직렬화 작업을 수행하는 함수임
# 직렬화란? > https://ko.wikipedia.org/wiki/%EC%A7%81%EB%A0%AC%ED%99%94
# 간단히 말해, 데이터를 다른 포맷으로 변환하는 것