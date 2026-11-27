"""Тесты для модуля utils."""

import json
from pathlib import Path

from src.utils import load_operations


def test_load_operations_reads_a_list_of_operations(tmp_path: Path) -> None:
    """Прочитать список операций из корректного JSON-файла."""
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps(expected), encoding="utf-8")

    assert load_operations(file_path) == expected


def test_load_operations_returns_empty_list_for_missing_file(tmp_path: Path) -> None:
    """Вернуть пустой список, если файла нет."""
    assert load_operations(tmp_path / "missing.json") == []


def test_load_operations_returns_empty_list_for_non_list_json(tmp_path: Path) -> None:
    """Вернуть пустой список, если корень JSON не является списком."""
    file_path = tmp_path / "operation.json"
    file_path.write_text(json.dumps({"id": 1}), encoding="utf-8")

    assert load_operations(file_path) == []


def test_load_operations_returns_empty_list_for_non_object_item(tmp_path: Path) -> None:
    """Вернуть пустой список, если элемент списка не является объектом."""
    file_path = tmp_path / "operations.json"
    file_path.write_text(
        json.dumps([{"id": 1}, "not an operation"]),
        encoding="utf-8",
    )

    assert load_operations(file_path) == []
