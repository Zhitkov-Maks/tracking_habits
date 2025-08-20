from http.client import HTTPException

from api.client import Client
from config import habit_url
from utils.create import create_header


async def get_list_comment(
    user_id: int,
    habit_id: int,
    page: int
) -> dict:
    """
    Request for a getting list of comments.
    :param habit_id: ID habit.
    :param user_id: ID user.
    :param page: The page you need to display.
    :return dict: A dictionary with a list of comment.
    """
    url: str = habit_url + (
        f"{habit_id}/comment/?page={page}&page_size=1"
    )
    client: Client = Client(url=url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.get()

    if status_code == 200:
        return response
    else:
        raise HTTPException(response.get("detail", {}).get("descr"))


async def request_for_save_comment(
    user_id: int,
    habit_id: int,
    data: dict[str, str]
) -> bool:
    """
    Request to save a comment from a habit.
    :param user_id: ID user.
    :param habit_id: ID habit.
    :return True: If request is success.
    :param data: Dictionary with a comment to send.
    """
    url: str = habit_url + f"{habit_id}/comment/"
    client: Client = Client(url=url, data=data)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.post()
    if status_code == 201:
        return True
    else:
        raise HTTPException(response.get("detail", {}).get("descr"))


async def delete_comment(comment_id: int, user_id: int) -> None:
    """
    Запрос на удаление комментария.
    :param comment_id: Идентификатор комментария.
    :param user_id: Telegram User ID.
    """
    url: str = habit_url + f"comment/{comment_id}"
    client: Client = Client(url=url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.delete()

    if status_code != 200:
        raise HTTPException(response.get("detail").get("descr"))
