import hashlib
from datetime import datetime as dt, UTC, timedelta, datetime

import jwt

from config import settings
from schemas.user import UserData


async def hash_password(
    password: str,
) -> str:
    return hashlib.md5(password.encode('utf-8')).hexdigest()


async def encode_jwt(
    user: UserData,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_days: int = settings.auth_jwt.access_token_expire_days,
    expire_timedelta: timedelta | None = None,
) -> str:
    now: datetime = dt.now(UTC)

    if expire_timedelta:
        expire = now + expire_timedelta

    else:
        expire = now + timedelta(days=expire_days)

    to_encode: dict = {
        "user_chat_id": user.user_chat_id,
        "username": user.username,
        "exp": expire,
        "iat":now,
    }

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


async def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
