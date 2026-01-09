from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from typing import Union
from datetime import timedelta, datetime, timezone

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()  # payload
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
