"""Модуль для маскирования номера карты и счёта."""


def get_mask_card_number(card_number: str) -> str:
    """Вернуть маску номера карты."""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Вернуть маску номера счёта."""
    return f"**{account_number[-4:]}"
