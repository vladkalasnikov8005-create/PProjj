"""Тесты для декоратора log."""

from pathlib import Path
from typing import Any

import pytest

from src.decorators import log


@log()
def add_numbers(x: int, y: int) -> int:
    """Сложить два числа."""
    return x + y


@log()
def fail_numbers(x: int, y: int) -> int:
    """Выбросить ошибку."""
    raise ValueError("плохо")


def test_log_console_ok(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверить успешный лог в консоль."""
    assert add_numbers(1, 2) == 3
    captured = capsys.readouterr()
    assert captured.out.strip() == "add_numbers ok"


def test_log_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверить лог ошибки в консоль."""
    with pytest.raises(ValueError):
        fail_numbers(1, 2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "fail_numbers error: ValueError. Inputs: (1, 2), {}"


def test_log_file_ok(tmp_path: Path) -> None:
    """Проверить успешный лог в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x: int, y: int) -> int:
        return x + y

    assert my_function(1, 2) == 3
    assert log_file.read_text(encoding="utf-8").strip() == "my_function ok"


def test_log_file_error(tmp_path: Path) -> None:
    """Проверить лог ошибки в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x: int, y: int) -> int:
        raise ZeroDivisionError("деление")

    with pytest.raises(ZeroDivisionError):
        my_function(1, 2)

    text = log_file.read_text(encoding="utf-8").strip()
    assert text == "my_function error: ZeroDivisionError. Inputs: (1, 2), {}"


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        ((1, 2), {}, "add_ok ok"),
        ((3, 4), {}, "add_ok ok"),
    ],
)
def test_log_console_parametrize(
    capsys: pytest.CaptureFixture[str],
    args: tuple[int, ...],
    kwargs: dict[str, Any],
    expected: str,
) -> None:
    """Проверить успешные вызовы с разными аргументами."""

    @log()
    def add_ok(x: int, y: int) -> int:
        return x + y

    add_ok(*args, **kwargs)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


def test_log_error_with_kwargs(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверить ошибку с именованными аргументами."""

    @log()
    def my_function(x: int, y: int) -> int:
        raise TypeError("тип")

    with pytest.raises(TypeError):
        my_function(x=1, y=2)
    captured = capsys.readouterr()
    assert "my_function error: TypeError. Inputs: (), {'x': 1, 'y': 2}" in captured.out
