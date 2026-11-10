"""Тесты для модуля processing."""

from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize("state", ["EXECUTED", "CANCELED", "PENDING"])
def test_filter_by_state(sample_operations: list[dict[str, Any]], state: str) -> None:
    """Проверить фильтр по разным статусам."""
    result = filter_by_state(sample_operations, state)
    assert result
    assert all(item["state"] == state for item in result)


def test_filter_by_state_default(sample_operations: list[dict[str, Any]]) -> None:
    """Проверить фильтр по умолчанию EXECUTED."""
    result = filter_by_state(sample_operations)
    assert all(item["state"] == "EXECUTED" for item in result)
    assert len(result) == 2


def test_filter_by_state_empty(sample_operations: list[dict[str, Any]]) -> None:
    """Проверить, что неизвестный статус даёт пустой список."""
    assert filter_by_state(sample_operations, "UNKNOWN") == []


def test_sort_by_date_descending(sample_operations: list[dict[str, Any]]) -> None:
    """Проверить сортировку по убыванию даты."""
    result = sort_by_date(sample_operations)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations: list[dict[str, Any]]) -> None:
    """Проверить сортировку по возрастанию даты."""
    result = sort_by_date(sample_operations, reverse=False)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates)


def test_sort_by_date_same_dates(sample_operations: list[dict[str, Any]]) -> None:
    """Проверить одинаковые даты."""
    same = [item for item in sample_operations if item["date"] == "2018-10-14T08:21:33.419441"]
    result = sort_by_date(same)
    assert len(result) == 2
    assert result[0]["date"] == result[1]["date"]


def test_sort_by_date_invalid() -> None:
    """Проверить некорректный формат даты."""
    with pytest.raises(ValueError):
        sort_by_date([{"date": "не дата"}])
