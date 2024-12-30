from typing import Dict

from decouple import config

BOT_TOKEN: str = config("TOKEN")
API_ADDRESS: str = config("API_ADDRESS")
BASE_URL: str = "/api/v1/"


register_url: str = API_ADDRESS + BASE_URL + "auth/registration/"
login_url: str = API_ADDRESS + BASE_URL + "auth/login/"
reset_url: str = API_ADDRESS + BASE_URL + "auth/request-password-reset/"
reset_password_url: str = API_ADDRESS + BASE_URL + "auth/reset-password/"
habit_url: str = API_ADDRESS + BASE_URL + "habits/"
tracking_url: str = API_ADDRESS + BASE_URL + "tracking/{habit_id}/"
remind_url: str = API_ADDRESS + BASE_URL + "remind/"

jwt_token_data: Dict[int, str] = {}
app_schedule: dict = {}
scheduler_ids: dict = {}

PAGE_SIZE: int = 10
