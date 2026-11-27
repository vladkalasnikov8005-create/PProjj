"""Загрузка банковских операций из JSON-файла."""

import json
import logging
from pathlib import Path
from typing import Any, cast

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

Operation = dict[str, Any]


def load_operations(file_path: str | Path) -> list[Operation]:
    """Загрузить список операций из JSON-файла.

    При ошибке чтения, некорректном JSON или неверной структуре вернуть пустой список.
    """
    try:
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as file:
            data: object = json.load(file)
    except (OSError, json.JSONDecodeError, UnicodeError):
        logger.exception("load_operations: не удалось прочитать файл %s", file_path)
        return []

    if not isinstance(data, list):
        logger.error("load_operations: в файле %s ожидался список операций", path.name)
        return []

    operations: list[Operation] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(
                "load_operations: запись %d в файле %s не является объектом",
                index,
                path.name,
            )
            return []
        operations.append(cast(Operation, item))

    logger.info(
        "load_operations: успешно загружено %d операций из файла %s",
        len(operations),
        path.name,
    )
    return operations
