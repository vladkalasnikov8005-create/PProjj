"""Загрузка банковских операций из JSON, CSV и XLSX."""

import csv
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

Operation = dict[str, Any]


def load_operations(file_path: str | Path) -> list[Operation]:
    """Загрузить операции из файла, выбрав формат по расширению."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")

    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_operations_from_json(path)
    if suffix == ".csv":
        return load_operations_from_csv(path)
    if suffix in {".xlsx", ".xlsm"}:
        return load_operations_from_xlsx(path)
    raise ValueError("Поддерживаются только файлы JSON, CSV и XLSX.")


def load_operations_from_json(file_path: str | Path) -> list[Operation]:
    """Загрузить список операций из JSON-файла."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8-sig") as json_file:
        payload: Any = json.load(json_file)

    records: list[Any] | None = None
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        for key in ("transactions", "operations", "data"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                records = candidate
                break
    else:
        raise ValueError("JSON-файл должен содержать список операций.")

    if records is None:
        raise ValueError("В JSON-файле не найден список операций.")
    return [_normalize_operation(record) for record in records if isinstance(record, dict)]


def load_operations_from_csv(file_path: str | Path) -> list[Operation]:
    """Загрузить операции из CSV-файла с автоматическим выбором разделителя."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        sample = csv_file.read(4096)
        csv_file.seek(0)
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
        except csv.Error:
            delimiter = ","
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        return [
            _normalize_operation(record)
            for record in reader
            if record and any(value not in (None, "") for value in record.values())
        ]


def load_operations_from_xlsx(file_path: str | Path) -> list[Operation]:
    """Загрузить операции из первого листа XLSX-файла."""
    from openpyxl import load_workbook  # type: ignore[import-untyped]

    path = Path(file_path)
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        worksheet = workbook.active
        rows = worksheet.iter_rows(values_only=True)
        headers = next(rows, None)
        if not headers:
            return []

        header_names = [str(header).strip() if header is not None else "" for header in headers]
        operations: list[Operation] = []
        for row in rows:
            record = {
                header: value
                for header, value in zip(header_names, row)
                if header and value is not None
            }
            if record:
                operations.append(_normalize_operation(record))
        return operations
    finally:
        workbook.close()


def _normalize_operation(record: dict[str, Any]) -> Operation:
    """Привести плоскую CSV/XLSX-строку к структуре банковской операции."""
    operation: Operation = {
        str(key).strip(): _normalize_cell(value)
        for key, value in record.items()
        if key is not None and str(key).strip()
    }

    flattened = {_canonical_key(key): value for key, value in operation.items()}
    amount = _first_value(
        flattened,
        ("_amount", "amount", "sum", "operation_amount_value"),
    )
    currency_name = _first_value(flattened, ("_currency_name", "currency_name"))
    currency_code = _first_value(flattened, ("_currency_code", "currency_code"))

    currency_value = operation.get("currency")
    if isinstance(currency_value, dict):
        currency_name = currency_name or currency_value.get("name")
        currency_code = currency_code or currency_value.get("code")
    elif isinstance(currency_value, str) and currency_value:
        currency_code = currency_code or currency_value
        currency_name = currency_name or currency_value

    operation_amount = operation.get("operationAmount", operation.get("operation_amount"))
    if isinstance(operation_amount, str):
        try:
            operation_amount = json.loads(operation_amount)
        except json.JSONDecodeError:
            operation_amount = None
    if isinstance(operation_amount, dict):
        nested_currency = operation_amount.get("currency", {})
        if isinstance(nested_currency, dict):
            currency_name = currency_name or nested_currency.get("name")
            currency_code = currency_code or nested_currency.get("code")
        amount = amount if amount is not None else operation_amount.get("amount")

    if amount is not None or currency_name is not None or currency_code is not None:
        currency_code = str(currency_code or currency_name or "")
        currency_name = str(currency_name or currency_code)
        operation["operationAmount"] = {
            "amount": str(amount) if amount is not None else "",
            "currency": {"name": currency_name, "code": currency_code},
        }

    if isinstance(operation_amount, dict):
        operation["operationAmount"] = operation_amount

    return operation


def _canonical_key(key: str) -> str:
    """Нормализовать имя колонки для распознавания плоских полей валюты."""
    normalized = re.sub(r"[\s-]+", "_", key.strip().lower())
    aliases = {
        "operationamount.amount": "_amount",
        "operation_amount.amount": "_amount",
        "operationamount_amount": "_amount",
        "operation_amount_amount": "_amount",
        "operationamount.currency.name": "_currency_name",
        "operation_amount.currency.name": "_currency_name",
        "operationamount_currency_name": "_currency_name",
        "operation_amount_currency_name": "_currency_name",
        "currency.name": "_currency_name",
        "operationamount.currency.code": "_currency_code",
        "operation_amount.currency.code": "_currency_code",
        "operationamount_currency_code": "_currency_code",
        "operation_amount_currency_code": "_currency_code",
        "currency.code": "_currency_code",
        "currencyname": "_currency_name",
        "currencycode": "_currency_code",
    }
    return aliases.get(normalized, normalized)


def _first_value(record: dict[str, Any], keys: tuple[str, ...]) -> Any:
    """Вернуть первое непустое значение из перечисленных колонок."""
    return next((record[key] for key in keys if record.get(key) not in (None, "")), None)


def _normalize_cell(value: Any) -> Any:
    """Преобразовать даты из таблиц в ISO-формат, остальные значения сохранить."""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value
