from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from config.database import collection_user
from schemas.users_schema import users_serializer
from models.users_model import User
from jose import jwt

router = APIRouter(
	tags=["users"]
)

# JWT 관련내용은 공식문서 (https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) 참고
# JWT에 대한 내용은 https://jwt.io/ 에서 확인 가능
# JWT란? 간단히 말해 토큰을 사용하여 정보를 안전하게 전달하는 방법 중 하나
# JWT 토큰은 3가지로 구성되어 있음
# 1. Header : 토큰의 타입과 해시 암호화 알고리즘으로 구성
# 2. Payload : 토큰에 담을 정보가 들어있는 부분
# 3. Signature : 일련의 문자열로, 토큰을 인코딩하고, 헤더의 인코딩 값, 페이로드의 인코딩 값을 합친 후, 비밀키로 해싱하여 생성
# JWT 토큰은 위의 3가지를 합친 문자열로 구성되어 있음

# JWT 토큰 만료 시간
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# JWT 토큰 암호화 키
SECRET_KEY = "secretkey825"
# JWT 토큰 암호화 알고리즘
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
		"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	}
	access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

	return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"]
    }

