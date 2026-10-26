from datetime import datetime
from typing import Any

Operation = dict[str, Any]


def filter_by_state(
    operations: list[Operation],
    state: str = "EXECUTED",
) -> list[Operation]:
    """Отфильтровать операции по статусу."""
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: list[Operation],
    reverse: bool = True,
) -> list[Operation]:
    """Отсортировать операции по дате."""
    return sorted(
        operations,
        key=lambda operation: datetime.fromisoformat(operation["date"]),
        reverse=reverse,
    )