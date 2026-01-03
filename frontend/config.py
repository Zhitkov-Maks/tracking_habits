from collections import defaultdict
from typing import Dict

from aiogram import Bot

from decouple import config


BOT_TOKEN = config("TOKEN")
API_ADDRESS = config("API_ADDRESS")
BASE_URL: str = "/api/v1/"

WORKER_BOT = Bot(token=BOT_TOKEN)


register_url: str = API_ADDRESS + BASE_URL + "auth/registration/"
login_url: str = API_ADDRESS + BASE_URL + "auth/login/"
logout_url: str = API_ADDRESS + BASE_URL + "auth/logout/"
reset_url: str = API_ADDRESS + BASE_URL + "auth/request-password-reset/"
reset_password_url: str = API_ADDRESS + BASE_URL + "auth/reset-password/"
habit_url: str = API_ADDRESS + BASE_URL + "habits/"
tracking_url: str = habit_url + "{habit_id}/tracking/"
remind_url: str = API_ADDRESS + BASE_URL + "reminds/"

jwt_token_data: Dict[int, dict] = {}
app_schedule: dict = {}
scheduler_ids: dict = {}

PAGE_SIZE: int = 10
