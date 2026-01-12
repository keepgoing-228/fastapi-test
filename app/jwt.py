from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from typing import Union
from datetime import timedelta, datetime, timezone

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app import exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()  # payload
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise exceptions.CredentialsDataWrong()
    except JWTError:
        raise exceptions.CredentialsDataWrong()

    return payload
