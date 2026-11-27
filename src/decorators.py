"""Модуль с декораторами."""

from collections.abc import Callable
from typing import Any


def log(filename: str | None = None) -> Callable:
    """Логировать работу функции в файл или в консоль."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(message, filename)
                raise
            _write_log(f"{func.__name__} ok", filename)
            return result

        return wrapper

    return decorator


def _write_log(message: str, filename: str | None) -> None:
    """Записать лог в файл или вывести в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message + "\n")
    else:
        print(message)
