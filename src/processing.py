"""Модуль фильтрации, сортировки и анализа банковских операций."""

import re
from collections import Counter
from datetime import datetime
from typing import Any

Operation = dict[str, Any]


def filter_by_state(
    operations: list[Operation],
    state: str = "EXECUTED",
) -> list[Operation]:
    """Отфильтровать операции по статусу без учёта регистра."""
    normalized_state = state.upper()
    return [
        operation
        for operation in operations
        if str(operation.get("state", "")).upper() == normalized_state
    ]


def sort_by_date(
    operations: list[Operation],
    reverse: bool = True,
) -> list[Operation]:
    """Отсортировать операции по дате."""
    return sorted(
        operations,
        key=lambda operation: datetime.fromisoformat(str(operation["date"])),
        reverse=reverse,
    )


def process_bank_search(data: list[Operation], search: str) -> list[Operation]:
    """Найти операции, в описании которых встречается строка поиска.

    Поиск выполняется регулярным выражением без учёта регистра. Ввод
    экранируется, чтобы специальные символы воспринимались буквально.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        operation
        for operation in data
        if isinstance(operation.get("description"), str)
        and pattern.search(operation["description"]) is not None
    ]


def process_bank_operations(
    data: list[Operation],
    categories: list[str],
) -> dict[str, int]:
    """Подсчитать количество операций для каждой категории из description."""
    category_set = set(categories)
    descriptions = (
        description
        for operation in data
        if isinstance((description := operation.get("description")), str)
        and description in category_set
    )
    counts = Counter(descriptions)
    return {category: counts[category] for category in categories}
