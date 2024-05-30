import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwk, jwt
from pydantic import BaseModel
import requests

from models import TokenPayload

# AWS Cognito 설정
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_REGION = os.getenv("COGNITO_REGION")
COGNITO_JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Cognito의 JWKS (JSON Web Key Set)를 가져옵니다.
jwks_client = requests.get(COGNITO_JWKS_URL).json()


def get_public_key(kid):
    for key in jwks_client["keys"]:
        if key["kid"] == kid:
            return jwk.construct(key).to_pem()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Public key not found"
    )


def verify_token(token: str):
    try:
        headers = jwt.get_unverified_header(token)
        public_key = get_public_key(headers["kid"])
        payload = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=COGNITO_APP_CLIENT_ID
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return TokenPayload(sub=payload["sub"], username=payload["username"])
