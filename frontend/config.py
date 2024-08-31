from decouple import config

BOT_TOKEN: str = config("TOKEN")
API_ADDRESS: str = config("API_ADDRESS")


register_url: str = API_ADDRESS + "/api/v1/auth/registration/"
login_url: str = API_ADDRESS + "/api/v1/auth/login/"
create_habit_url: str = API_ADDRESS + "/api/v1/habits/new/"
get_list_habits_url: str = API_ADDRESS + "/api/v1/habits/list/"

jwt_token_data: dict = {}
