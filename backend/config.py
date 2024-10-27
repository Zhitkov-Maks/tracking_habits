import os

from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_days: int = 30


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
