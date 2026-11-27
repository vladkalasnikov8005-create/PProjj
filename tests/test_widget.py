"""Тесты для модуля widget."""

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счёт 35383033474447895560", "Счёт **5560"),
    ],
)
def test_mask_account_card(info: str, expected: str) -> None:
    """Проверить маскировку карты и счёта."""
    assert mask_account_card(info) == expected


def test_mask_account_card_empty() -> None:
    """Проверить пустую строку."""
    assert mask_account_card("") == ""
    assert mask_account_card("   ") == ""


def test_mask_account_card_without_number() -> None:
    """Проверить строку без номера."""
    assert mask_account_card("Visa") == "Visa"


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2020-01-01T00:00:00", "01.01.2020"),
    ],
)
def test_get_date(raw: str, expected: str) -> None:
    """Проверить преобразование даты."""
    assert get_date(raw) == expected


def test_get_date_empty() -> None:
    """Проверить строку без даты."""
    assert get_date("") == ""
    assert get_date("нет даты") == ""


def test_get_date_bad_format() -> None:
    """Проверить нестандартную строку с T."""
    assert get_date("11/07/2018T12:00") == ""
