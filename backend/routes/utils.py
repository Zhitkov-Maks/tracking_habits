import hashlib
import logging
from datetime import datetime as dt, UTC, timedelta, datetime
from email.mime.text import MIMEText
from typing import Dict

import aiosmtplib
import jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from starlette import status

from config import settings, EMAIL, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT
from schemas.user import UserData
from database.revoked import RevokedToken


logging.basicConfig(level=logging.INFO)


async def hash_password(
    password: str,
) -> str:
    """
    Password hashing function.
    :param password: The password that needs to be hashed.
    :return str: Hash as a string.
    """
    return hashlib.md5(password.encode("utf-8")).hexdigest()


async def is_token_revoked(session: AsyncSession, token: str) -> bool:
    """
    Checks whether the token has been revoked.
    """
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    count = await session.scalar(
        select(func.count())
        .where(RevokedToken.token == token_hash)
        .where(RevokedToken.expires_at >= datetime.now(UTC))
    )
    return count > 0


async def revoke_token(
    session: AsyncSession,
    token: str,
    expires_at: datetime
) -> None:
    """
    Adds the token to the blacklist with upsert logic.
    """
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)

    stmt = insert(RevokedToken).values(
        token=token_hash,
        expires_at=expires_at
    ).on_conflict_do_update(
        index_elements=['token'],
        set_={'expires_at': expires_at}
    )

    await session.execute(stmt)
    await session.commit()


async def encode_jwt(
    user: UserData,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_days: int = settings.auth_jwt.access_token_expire_days,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Encodes user data. Returns the token.

    :param user: Received user data.
    :param private_key: A private key for encoding.
    :param expire_days: The number of days during which the token is valid.
    :param expire_timedelta: timedelta из datetime
    :param algorithm: The type of encryption algorithm.
    :return str: Returns a string containing the token.
    """
    now: datetime = dt.now(UTC)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(days=expire_days)

    to_encode: Dict[str, str] = {
        "email": user.email,
        "password": user.password,
        "exp": expire,
        "jti": hashlib.sha256(
            f"{user.email}{now.timestamp()}".encode()
        ).hexdigest()  # Unique token ID
    }

    encoded: str = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


async def decode_jwt(
    token: str | bytes,
    session: AsyncSession,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> Dict[str, str]:
    """
    Decodes the send token.
    Returns a dictionary with user data.
    :param token: The send authentication token.
    :param public_key: The key for decoding.
    :param algorithm: The type of encryption algorithm.
    :return dict: Returns a dictionary with user data.
    """
    # Checking if the token has been revoked.
    if await is_token_revoked(session, token):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "description": "Токен был удален.",
            },
        )

    decoded: Dict[str, str] = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


async def send_email(to_email: str, subject: str, body: str) -> None:
    """
    The function sends an email to the user about the successful
    password change.
    :param to_email: user's email.
    :param subject: Email subject.
    :param body: Email body.
    :return None:
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    try:
        await aiosmtplib.send(
            msg,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL,
            password=EMAIL_PASSWORD,
            start_tls=True
        )
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
