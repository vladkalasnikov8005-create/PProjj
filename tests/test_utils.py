"""Тесты загрузки операций из JSON, CSV и XLSX."""

import json
from pathlib import Path

import pytest
from openpyxl import Workbook  # type: ignore[import-untyped]

from src.utils import load_operations


def test_load_operations_from_json(tmp_path: Path) -> None:
    """JSON-список сохраняет структуру вложенной суммы."""
    path = tmp_path / "operations.json"
    expected = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод",
            "operationAmount": {
                "amount": "10.50",
                "currency": {"name": "USD", "code": "USD"},
            },
        }
    ]
    path.write_text(json.dumps(expected, ensure_ascii=False), encoding="utf-8")

    assert load_operations(path) == expected


def test_load_operations_from_json_object(tmp_path: Path) -> None:
    """JSON-объект с ключом transactions тоже поддерживается."""
    path = tmp_path / "transactions.json"
    path.write_text(
        json.dumps({"transactions": [{"description": "Покупка"}]}, ensure_ascii=False),
        encoding="utf-8",
    )

    assert load_operations(path) == [{"description": "Покупка"}]


def test_load_operations_from_csv(tmp_path: Path) -> None:
    """Плоские поля CSV собираются во вложенную структуру суммы."""
    path = tmp_path / "transactions.csv"
    path.write_text(
        "id,state,date,amount,currency_name,currency_code,description,from,to\n"
        '1,EXECUTED,2019-01-02T12:00:00,10.50,USD,USD,Перевод,Счет 1234567890123456,Счет 9876543210987654\n',
        encoding="utf-8",
    )

    result = load_operations(path)

    assert result[0]["id"] == "1"
    assert result[0]["operationAmount"] == {
        "amount": "10.50",
        "currency": {"name": "USD", "code": "USD"},
    }
    assert result[0]["description"] == "Перевод"


def test_load_operations_from_semicolon_csv(tmp_path: Path) -> None:
    """CSV с точкой с запятой в качестве разделителя тоже читается."""
    path = tmp_path / "transactions.csv"
    path.write_text("description;state\nПокупка;EXECUTED\n", encoding="utf-8")

    assert load_operations(path) == [{"description": "Покупка", "state": "EXECUTED"}]


def test_load_operations_from_xlsx(tmp_path: Path) -> None:
    """Первая таблица XLSX загружается и нормализуется."""
    path = tmp_path / "transactions.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["id", "state", "date", "amount", "currency_name", "currency_code", "description"])
    worksheet.append([1, "EXECUTED", "2019-01-02T12:00:00", 10.5, "руб.", "RUB", "Открытие вклада"])
    workbook.save(path)
    workbook.close()

    result = load_operations(path)

    assert result[0]["operationAmount"] == {
        "amount": "10.5",
        "currency": {"name": "руб.", "code": "RUB"},
    }
    assert result[0]["description"] == "Открытие вклада"


def test_load_operations_from_empty_xlsx(tmp_path: Path) -> None:
    """Пустой лист XLSX возвращает пустой список."""
    path = tmp_path / "empty.xlsx"
    workbook = Workbook()
    workbook.save(path)
    workbook.close()

    assert load_operations(path) == []


def test_load_operations_missing_file(tmp_path: Path) -> None:
    """Для отсутствующего файла поднимается FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_operations(tmp_path / "missing.json")


def test_load_operations_unsupported_extension(tmp_path: Path) -> None:
    """Неподдерживаемое расширение даёт понятную ошибку."""
    path = tmp_path / "operations.txt"
    path.write_text("data", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON, CSV и XLSX"):
        load_operations(path)


def test_load_operations_invalid_json(tmp_path: Path) -> None:
    """Повреждённый JSON не маскируется под пустой список."""
    path = tmp_path / "operations.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_operations(path)
