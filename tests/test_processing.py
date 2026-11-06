"""Тесты для модуля processing."""

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_uses_executed_by_default() -> None:
    """Проверить фильтр по статусу EXECUTED."""
    operations = [
        {"state": "EXECUTED", "date": "2020-01-01"},
        {"state": "CANCELED", "date": "2020-01-02"},
    ]

    assert filter_by_state(operations) == [operations[0]]


def test_filter_by_state_accepts_another_state() -> None:
    """Проверить фильтр по другому статусу."""
    operations = [
        {"state": "EXECUTED", "date": "2020-01-01"},
        {"state": "CANCELED", "date": "2020-01-02"},
    ]

    assert filter_by_state(operations, "CANCELED") == [operations[1]]


def test_sort_by_date_descending_by_default() -> None:
    """Проверить сортировку по дате по убыванию."""
    older = {"date": "2020-01-01"}
    newer = {"date": "2020-01-02"}

    assert sort_by_date([older, newer]) == [newer, older]
