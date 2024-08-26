import hashlib


async def hash_password(
    password: str,
) -> str:
    return hashlib.md5(password.encode('utf-8')).hexdigest()
