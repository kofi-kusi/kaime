from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from .config import security_settings

oauth2scheme_customer = OAuth2PasswordBearer(
    tokenUrl="/user/token", scheme_name="User"
)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


def generate_access_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        key=security_settings.JWT_SECRET_KEY,
        algorithm=security_settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )