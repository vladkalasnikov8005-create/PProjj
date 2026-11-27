"""Проверки логирования в модулях masks и utils."""

import json
import logging
import re
from pathlib import Path

import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.masks import logger as masks_logger
from src.utils import load_operations
from src.utils import logger as utils_logger

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"


@pytest.mark.parametrize(
    ("module_logger", "log_path"),
    [
        (masks_logger, LOG_DIR / "masks.log"),
        (utils_logger, LOG_DIR / "utils.log"),
    ],
)
def test_logger_configuration(module_logger: logging.Logger, log_path: Path) -> None:
    """Проверить отдельный файловый логер, уровень и формат записи."""
    assert module_logger.level == logging.DEBUG
    assert module_logger.propagate is False
    assert module_logger is not logging.getLogger()

    file_handlers = [
        handler
        for handler in module_logger.handlers
        if isinstance(handler, logging.FileHandler)
    ]
    assert len(file_handlers) == 1

    handler = file_handlers[0]
    assert Path(handler.baseFilename) == log_path
    assert handler.mode == "w"
    assert handler.formatter is not None

    record = logging.LogRecord(
        name=module_logger.name,
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="test message",
        args=(),
        exc_info=None,
    )
    formatted = handler.formatter.format(record)
    assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - ", formatted)
    assert module_logger.name in formatted
    assert "INFO" in formatted
    assert "test message" in formatted


def test_mask_card_success_is_logged() -> None:
    """Успешное маскирование карты записывается в masks.log."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

    log_text = (LOG_DIR / "masks.log").read_text(encoding="utf-8")
    assert "src.masks - INFO -" in log_text
    assert "get_mask_card_number" in log_text


def test_mask_card_error_is_logged() -> None:
    """Ошибка маскирования карты записывается и пробрасывается дальше."""
    with pytest.raises(TypeError):
        get_mask_card_number(None)  # type: ignore[arg-type]

    log_text = (LOG_DIR / "masks.log").read_text(encoding="utf-8")
    assert "src.masks - ERROR -" in log_text
    assert "ошибка при маскировании номера карты" in log_text


def test_mask_account_success_is_logged() -> None:
    """Успешное маскирование счёта записывается в masks.log."""
    assert get_mask_account("73654108430135874305") == "**4305"

    log_text = (LOG_DIR / "masks.log").read_text(encoding="utf-8")
    assert "src.masks - INFO -" in log_text
    assert "get_mask_account" in log_text


def test_mask_account_error_is_logged() -> None:
    """Ошибка маскирования счёта записывается и пробрасывается дальше."""
    with pytest.raises(TypeError):
        get_mask_account(None)  # type: ignore[arg-type]

    log_text = (LOG_DIR / "masks.log").read_text(encoding="utf-8")
    assert "src.masks - ERROR -" in log_text
    assert "ошибка при маскировании номера счёта" in log_text


def test_load_operations_success_is_logged(tmp_path: Path) -> None:
    """Успешная загрузка JSON записывается в utils.log."""
    expected = [{"id": 1, "state": "EXECUTED"}]
    operations_file = tmp_path / "operations.json"
    operations_file.write_text(json.dumps(expected), encoding="utf-8")

    assert load_operations(operations_file) == expected

    log_text = (LOG_DIR / "utils.log").read_text(encoding="utf-8")
    assert "src.utils - INFO -" in log_text
    assert "load_operations: успешно загружено 1 операций" in log_text


def test_load_operations_error_is_logged(tmp_path: Path) -> None:
    """Ошибка чтения JSON записывается уровнем ERROR и возвращает пустой список."""
    operations_file = tmp_path / "invalid.json"
    operations_file.write_text("{broken json", encoding="utf-8")

    assert load_operations(operations_file) == []

    log_text = (LOG_DIR / "utils.log").read_text(encoding="utf-8")
    assert "src.utils - ERROR -" in log_text
    assert "load_operations: не удалось прочитать файл" in log_text
