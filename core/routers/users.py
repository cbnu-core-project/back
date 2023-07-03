from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from config.database import collection_user
from schemas.users_schema import users_serializer
from models.users_model import User
from jose import jwt, JWTError

router = APIRouter(
	tags=["users"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 15
SECRET_KEY = "secretkey825"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/api/register")
def user_register(user: User):
	if(users_serializer(collection_user.find({"username": user.username}))):
		raise HTTPException(status_code=409,
							detail="이미 존재하는 사용자입니다.")
	collection_user.insert_one({"username": user.username,
								"password": pwd_context.hash(user.password),
								"nickname": user.nickname})
	return "회원가입 성공!"


@router.post("/api/login")
def login_for_acess_token(form_data: OAuth2PasswordRequestForm = Depends()):
	# 데이터베이스에서 유저데이터 가져오기
	user = users_serializer(collection_user.find({"username": form_data.username}))
	# 데이터베이스에 데이터가 있다면, user 데이터에 user 1개 저장
	if user:
		user = user[0]
	if not user or not pwd_context.verify(form_data.password, user["password"]):
		raise HTTPException(
			status_code=401,
			detail="잘못 된 username, password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	# access token 만들기
	data = {
		"sub": user["username"],
		"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
	}
	access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

	return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
		"clubs": user["clubs"]
    }


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login")
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

		return { "payload": payload, "user": user }
	except JWTError:
		raise HTTPException(status_code=401, detail="유효하지 않은 토큰이다.2")

# 보호된 엔드포인트
@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_schema)):
	payload = verify_token(token).get("payload")
	# 토큰이 유효하다면, 여기에서 필요한 처리를 수행합니다.
	print('토큰 유효한듯?')
	return token