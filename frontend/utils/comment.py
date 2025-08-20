async def generate_message_answer(
    data: dict[str, list[dict]]
) -> tuple[str, bool, int]:
    """
    Формирует строку для ответа пользователю, а также сообщает
    есть ли еще записи.

    :param data: Словарь содержащий список комментариев.
    """
    message = "*" * 40 + "\n\n"
    exists_next_page = False
    list_comments: list[dict] = data.get("data", [])
    if len(list_comments) < 1:
        return "Коментарий не найден.", exists_next_page, 0

    message += f"Дата: {list_comments[0]["created_at"][:10]}\n"
    message += f"{list_comments[0]["body"]}\n\n"
    message += "*" * 40
    if len(list_comments) > 1:
        exists_next_page = True

    return message, exists_next_page, list_comments[0]["id"]
