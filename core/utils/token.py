from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from config.database import collection_user
from schemas.users_schema import users_serializer
from jose import jwt, JWTError


ACCESS_TOKEN_EXPIRE_MINUTES = 15
SECRET_KEY = "secretkey825"
ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login")

# access token 만들기
def create_token(user):
	data = {
		"sub": user["username"],
		"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
	}
	access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
	return access_token

# 토큰 검증 함수
def verify_token(token: str = Depends(oauth2_schema)):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		sub = payload.get("sub")

		if sub is None:
			raise HTTPException(status_code=401, detail="로그인 되어있지 않다.")

		if sub:
			user = users_serializer(collection_user.find({"username": sub}))
			if user is None:
				raise HTTPException(status_code=401, detail="유효하지 않은 토큰이다.1")

		exp = payload.get("exp")
		if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
			raise HTTPException(status_code=401, detail="토큰이 이미 만기되었다.")

		return user[0]  # user는 dict형태로 반환
	except JWTError:
		raise HTTPException(status_code=401, detail="유효하지 않은 토큰이다.2")

# 스케줄을 작성/수정하기 위한 권한 확인, 내가 속해있는 동아리가 맞는 지 확인
def verify_authority(club_objid: str, token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	# 현재 속해 있는 클럽(동아리)와 data(post, schedule)추가/수정 대상의 동아리 비교
	if club_objid in user.get("clubs"):
		return user

	raise HTTPException(status_code=401, detail="속해있는 동아리가 아니다.")



