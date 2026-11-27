"""Тесты поиска и подсчёта категорий операций."""

from typing import Any

from src.processing import process_bank_operations, process_bank_search


def test_process_bank_search_is_case_insensitive() -> None:
    """Поиск находит описание без учёта регистра."""
    operations: list[dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "ПЕРЕВОД с карты"},
        {"state": "EXECUTED"},
    ]

    result = process_bank_search(operations, "перевод")

    assert result == [operations[0], operations[2]]


def test_process_bank_search_treats_query_as_literal() -> None:
    """Спецсимволы в поисковом тексте воспринимаются буквально."""
    operations: list[dict[str, Any]] = [
        {"description": "Платёж по карте Visa."},
        {"description": "Платёж по карте Visa!"},
    ]

    assert process_bank_search(operations, "Visa.") == [operations[0]]


def test_process_bank_search_empty_query_returns_described_operations() -> None:
    """Пустая строка совпадает с любым строковым описанием."""
    operations: list[dict[str, Any]] = [
        {"description": "Перевод"},
        {"description": ""},
        {"description": None},
        {},
    ]

    assert process_bank_search(operations, "") == operations[:2]


def test_process_bank_operations_counts_requested_categories() -> None:
    """Подсчёт включает нулевые категории и игнорирует прочие описания."""
    operations: list[dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Платёж по карте"},
        {"state": "EXECUTED"},
    ]

    result = process_bank_operations(
        operations,
        ["Перевод организации", "Открытие вклада", "Неизвестная категория"],
    )

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Неизвестная категория": 0,
    }


def test_process_bank_operations_empty_inputs() -> None:
    """Для пустого списка операций все запрошенные счётчики равны нулю."""
    assert process_bank_operations([], ["Перевод", "Вклад"]) == {"Перевод": 0, "Вклад": 0}
