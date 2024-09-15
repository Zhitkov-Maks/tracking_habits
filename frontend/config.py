from decouple import config

BOT_TOKEN: str = config("TOKEN")
API_ADDRESS: str = config("API_ADDRESS")


register_url: str = API_ADDRESS + "/api/v1/auth/registration/"
login_url: str = API_ADDRESS + "/api/v1/auth/login/"
habit_url: str = API_ADDRESS + "/api/v1/habits/"
tracking_url: str = API_ADDRESS + "/api/v1/tracking/{habit_id}/"
remind_url: str = API_ADDRESS + "/api/v1/remind/"

jwt_token_data: dict = {}
app_schedule: dict = {}
scheduler_ids: dict = {}
