"""Модуль для маскирования карт/счетов и преобразования даты."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Замаскировать номер карты или счёта в строке."""
    if not account_info.strip():
        return ""

    parts = account_info.split()
    if len(parts) < 2:
        return account_info

    number = parts[-1]
    title = " ".join(parts[:-1])
    lowered = account_info.lower()

    if "счет" in lowered or "счёт" in lowered:
        return f"{title} {get_mask_account(number)}"
    return f"{title} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """Вернуть дату в формате ДД.ММ.ГГГГ."""
    if not date_string or "T" not in date_string:
        return ""

    date_part = date_string.split("T")[0]
    parts = date_part.split("-")
    if len(parts) != 3:
        return ""

    year, month, day = parts
    return f"{day}.{month}.{year}"
