"""Модуль для маскирования номера карты и счёта."""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

file_handler = logging.FileHandler(
    LOG_DIR / "masks.log",
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Вернуть маску номера карты."""
    try:
        masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    except Exception:
        logger.exception("get_mask_card_number: ошибка при маскировании номера карты")
        raise

    logger.info("get_mask_card_number: номер карты успешно замаскирован")
    return masked_number


def get_mask_account(account_number: str) -> str:
    """Вернуть маску номера счёта."""
    try:
        masked_number = f"**{account_number[-4:]}"
    except Exception:
        logger.exception("get_mask_account: ошибка при маскировании номера счёта")
        raise

    logger.info("get_mask_account: номер счёта успешно замаскирован")
    return masked_number
