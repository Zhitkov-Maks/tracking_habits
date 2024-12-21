from http.client import HTTPException
from api.client import Client
from utils.create import create_header
from config import habit_url


async def get_list_habits(user_id: int,is_active: int = 1) -> dict:
    """
    Request for a getting list of habits.
    :param user_id: ID user.
    :param is_active: It is needed to show either habits
                        from the archive or active.
    :return dict: A dictionary with a list of habits.
    """
    url: str = habit_url + f"?is_active={is_active}"
    client: Client = Client(url=url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response= await client.get()

    if status_code == 200:
        return response
    else:
        raise HTTPException(response.get("detail").get("descr"))


async def get_full_info(habit_id: int, user_id: int) -> dict | tuple:
    """
    Request for getting full information about a particular habit.
    :param habit_id: ID habit.
    :param user_id: ID user.
    :return dict: A dictionary with complete data about the habit.
    """
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url=url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.get()

    if status_code == 200:
        return response
    else:
        raise HTTPException(response.get("detail").get("descr"))


async def delete_habit(habit_id: int, user_id: int) -> None:
    """
    A request to remove a specific habit.
    :param habit_id: The ID of the habit.
    :param user_id: Telegram User ID.
    """
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url=url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.delete()

    if status_code != 200:
        raise HTTPException(response.get("detail").get("descr"))


async def archive_habit(habit_id: int, user_id: int, is_active: bool) -> None:
    """
    Request to change the status of a habit.
    :param habit_id: The ID of the habit.
    :param user_id: The telegram user ID.
    :param is_active: It is needed to change the status of a habit.
    """
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url=url, data={"is_active": is_active})
    client.header.update({"Authorization": await create_header(user_id)})
    status_code, response = await client.patch()

    if status_code != 200:
        raise HTTPException(response.get("detail").get("descr"))
