"""Тесты для модуля masks."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        ("1234567890123456", "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number(number: str, expected: str) -> None:
    """Проверить маскирование номера карты."""
    assert get_mask_card_number(number) == expected


def test_get_mask_card_number_from_fixture(card_number: str) -> None:
    """Проверить маску карты из фикстуры."""
    assert get_mask_card_number(card_number) == "7000 79** **** 6361"


def test_get_mask_card_number_empty() -> None:
    """Проверить пустую строку вместо номера карты."""
    result = get_mask_card_number("")
    assert isinstance(result, str)
    assert "*" in result


def test_get_mask_card_number_short() -> None:
    """Проверить короткий номер карты."""
    result = get_mask_card_number("123")
    assert isinstance(result, str)
    assert "*" in result


@pytest.mark.parametrize(
    "number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("00000000000000000001", "**0001"),
    ],
)
def test_get_mask_account(number: str, expected: str) -> None:
    """Проверить маскирование номера счёта."""
    assert get_mask_account(number) == expected


def test_get_mask_account_from_fixture(account_number: str) -> None:
    """Проверить маску счёта из фикстуры."""
    assert get_mask_account(account_number) == "**4305"


def test_get_mask_account_short() -> None:
    """Проверить короткий номер счёта."""
    assert get_mask_account("12") == "**12"
