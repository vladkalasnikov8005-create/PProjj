"""Тесты для модуля generators."""

from collections.abc import Iterator
from typing import Any

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency(
    sample_transactions: list[dict[str, Any]],
    currency: str,
    expected_count: int,
) -> None:
    """Проверить фильтр по валюте."""
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count
    assert all(
        item["operationAmount"]["currency"]["code"] == currency for item in result
    )


def test_filter_by_currency_usd_first(
    sample_transactions: list[dict[str, Any]],
) -> None:
    """Проверить, что генератор отдаёт USD по next()."""
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    assert isinstance(usd_transactions, Iterator)
    first = next(usd_transactions)
    second = next(usd_transactions)
    assert first["id"] == 939719570
    assert second["id"] == 142264268


def test_filter_by_currency_empty() -> None:
    """Проверить пустой список транзакций."""
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_no_amount() -> None:
    """Проверить транзакцию без operationAmount."""
    data = [{"id": 1, "description": "нет суммы"}]
    assert list(filter_by_currency(data, "USD")) == []


def test_transaction_descriptions(
    sample_transactions: list[dict[str, Any]],
) -> None:
    """Проверить описания из примера задания."""
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


@pytest.mark.parametrize(
    "data, expected",
    [
        ([], []),
        ([{"description": "Перевод организации"}], ["Перевод организации"]),
        (
            [{"description": "A"}, {"description": "B"}],
            ["A", "B"],
        ),
    ],
)
def test_transaction_descriptions_count(
    data: list[dict[str, Any]],
    expected: list[str],
) -> None:
    """Проверить разное количество транзакций, включая пустой список."""
    assert list(transaction_descriptions(data)) == expected


def test_transaction_descriptions_next(
    sample_transactions: list[dict[str, Any]],
) -> None:
    """Проверить выдачу описаний по next()."""
    descriptions = transaction_descriptions(sample_transactions)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (9999, 10000, ["0000 0000 0000 9999", "0000 0000 0001 0000"]),
    ],
)
def test_card_number_generator(start: int, stop: int, expected: list[str]) -> None:
    """Проверить номера карт в диапазоне."""
    result = list(card_number_generator(start, stop))
    assert result == expected


def test_card_number_generator_format() -> None:
    """Проверить формат XXXX XXXX XXXX XXXX."""
    number = next(card_number_generator(1, 1))
    parts = number.split()
    assert len(parts) == 4
    assert all(len(part) == 4 and part.isdigit() for part in parts)
    assert len(number.replace(" ", "")) == 16


def test_card_number_generator_stop() -> None:
    """Проверить, что генерация заканчивается на stop."""
    result = list(card_number_generator(3, 4))
    assert result[-1] == "0000 0000 0000 0004"
    with pytest.raises(StopIteration):
        gen = card_number_generator(3, 4)
        next(gen)
        next(gen)
        next(gen)
