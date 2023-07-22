import requests
import typing as t

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette import status


# We will handle a missing token ourselves
get_bearer_token = HTTPBearer(auto_error=False)

KAKAO_USERINFO_URL = 'https://kapi.kakao.com/v2/user/me'
NAVER_USERINFO_URL = "https://openapi.naver.com/v1/nid/me"

class UnauthorizedMessage(BaseModel):
	detail: str = "유효하지 않는 토큰이다."

def verify_common_token_and_get_unique_id(
    auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    # 토큰 자체가 없다면 401
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )

    token = auth.credentials
    headers = {'Authorization': 'Bearer ' + token }

    # 토큰 검증 (1. 카카오)
    response = requests.get(KAKAO_USERINFO_URL, headers=headers)
    if response.ok:
        id = response.json().get('id')
        return f"kakao_{id}"

    # 토큰 검증 (2. 네이버)
    response = requests.get(NAVER_USERINFO_URL, headers=headers)
    if response.ok:
        id = response.json().get('response').get('id')
        return f"naver_{id}"

    # 토큰이 유효하지 않다면 401
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )