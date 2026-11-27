"""Интеграционные тесты консольного интерфейса."""

import json
from pathlib import Path

import pytest

from src.main import format_operation, main


def test_format_operation_masks_accounts_and_formats_amount() -> None:
    """Строка операции содержит дату, описание, маскированные реквизиты и сумму."""
    operation = {
        "date": "2019-12-08T12:00:00",
        "description": "Открытие вклада",
        "to": "Счет 1234567890123456",
        "operationAmount": {
            "amount": "40542.00",
            "currency": {"name": "руб.", "code": "RUB"},
        },
    }

    result = format_operation(operation)

    assert "08.12.2019 Открытие вклада" in result
    assert "Счет **3456" in result
    assert "Сумма: 40542 руб." in result


def test_main_filters_by_status_currency_and_description(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Интерфейс применяет статус, валюту и текстовый поиск."""
    path = tmp_path / "operations.json"
    operations = [
        {
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46",
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
        },
        {
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05",
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
        },
        {
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25",
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
        },
    ]
    path.write_text(json.dumps(operations, ensure_ascii=False), encoding="utf-8")
    answers = iter(["1", "executed", "нет", "да", "да", "счета"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    main({"1": path})

    output = capsys.readouterr().out
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "Перевод со счета на счет" in output
    assert "Сумма: 43318.34 руб." in output
    assert "Перевод организации" not in output


def test_main_repeats_after_invalid_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Неверный статус сообщает об ошибке и повторно запрашивает ввод."""
    path = tmp_path / "operations.json"
    path.write_text(
        json.dumps([{"state": "EXECUTED", "description": "Покупка"}], ensure_ascii=False),
        encoding="utf-8",
    )
    answers = iter(["1", "wrong", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    main({"1": path})

    output = capsys.readouterr().out
    assert 'Статус операции "wrong" недоступен.' in output
    assert "Всего банковских операций в выборке: 1" in output


def test_main_handles_empty_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Для пустого результата выводится предусмотренное заданием сообщение."""
    path = tmp_path / "operations.json"
    path.write_text(
        json.dumps([{"state": "CANCELED", "description": "Покупка"}], ensure_ascii=False),
        encoding="utf-8",
    )
    answers = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    main({"1": path})

    assert "Не найдено ни одной транзакции" in capsys.readouterr().out


def test_main_retries_invalid_menu_and_sort_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Неверные ответы меню и сортировки не прерывают программу."""
    path = tmp_path / "operations.json"
    path.write_text(
        json.dumps(
            [
                {"state": "EXECUTED", "date": "2019-01-02T12:00:00", "description": "A"},
                {"state": "EXECUTED", "date": "2018-01-02T12:00:00", "description": "B"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    answers = iter(["9", "1", "EXECUTED", "да", "по дате", "по возрастанию", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    main({"1": path})

    output = capsys.readouterr().out
    assert "Неверный пункт меню" in output
    assert "Введите «по возрастанию» или «по убыванию»" in output
    assert output.index("02.01.2018 B") < output.index("02.01.2019 A")
