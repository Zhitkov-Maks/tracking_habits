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
    """
    Кодирует данные о пользователе. Возвращает токен.
    :param user: Пришедшие данные о пользователе.
    :param private_key: Приватный ключ для кодирования.
    :param expire_days: Количество дней, в течении которого действителен токен
    :param expire_timedelta: timedelta из datetime
    :param algorithm: Тип алгоритма шифрования.
    :return str: Возвращает строку, содержащую токен.
    """
    now: datetime = dt.now(UTC)

    if expire_timedelta:
        expire = now + expire_timedelta

    else:
        expire = now + timedelta(days=expire_days)

    to_encode: dict = {
        "user_chat_id": user.user_chat_id,
        "username": user.username,
        "password": user.password,
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
    """
    Декодирует присланный токен.
    Возвращает словарь сданными о пользователе.
    :param token: Присланный токен для аутентификации
    :param public_key: Ключ для декодирования.
    :param algorithm: Тип алгоритма шифрования.
    :return dict: Возвращает словарь с данными о пользователе.
    """
    decoded: dict = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
