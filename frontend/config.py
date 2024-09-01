from decouple import config

BOT_TOKEN: str = config("TOKEN")
API_ADDRESS: str = config("API_ADDRESS")


register_url: str = API_ADDRESS + "/api/v1/auth/registration/"
login_url: str = API_ADDRESS + "/api/v1/auth/login/"
create_habit_url: str = API_ADDRESS + "/api/v1/habits/new/"
get_list_habits_url: str = API_ADDRESS + "/api/v1/habits/list/"
get_detail_info: str = API_ADDRESS + "/api/v1/habits/"
delete_habit_url: str = API_ADDRESS + "/api/v1/habits/{habit_id}/delete/"
habits_to_archive_url: str = API_ADDRESS + "/api/v1/habits/{habit_id}/patch/"
add_tracking_url: str = API_ADDRESS + "/api/v1/tracking/{habit_id}/add/"
clean_all_tracking_url: str = API_ADDRESS + "/api/v1/tracking/{habit_id}/delete/"
habits_to_update_url: str = API_ADDRESS + "/api/v1/habits/{habit_id}/update/"

jwt_token_data: dict = {}
