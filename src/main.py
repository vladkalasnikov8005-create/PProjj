"""Интерактивная программа выбора и фильтрации банковских операций."""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import load_operations
from src.widget import mask_account_card

Operation = dict[str, Any]

MENU = (
    "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
    "Выберите необходимый пункт меню:\n"
    "1. Получить информацию о транзакциях из JSON-файла\n"
    "2. Получить информацию о транзакциях из CSV-файла\n"
    "3. Получить информацию о транзакциях из XLSX-файла"
)

FILE_OPTIONS: dict[str, tuple[str, Path]] = {
    "1": ("JSON", Path("data/operations.json")),
    "2": ("CSV", Path("data/transactions.csv")),
    "3": ("XLSX", Path("data/transactions_excel.xlsx")),
}
VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}
YES_ANSWERS = {"да", "д", "yes", "y"}
NO_ANSWERS = {"нет", "н", "no", "n"}


def main(file_paths: dict[str, str | Path] | None = None) -> None:
    """Загрузить, отфильтровать и вывести операции по выбору пользователя."""
    print(MENU)
    file_choice = _ask_file_type()
    file_label, default_path = FILE_OPTIONS[file_choice]
    print(f"Для обработки выбран {file_label}-файл.")

    path = Path(file_paths[file_choice]) if file_paths and file_choice in file_paths else default_path
    try:
        operations = load_operations(path)
    except (OSError, ValueError, TypeError) as error:
        print(f"Не удалось загрузить операции: {error}")
        return

    status = _ask_status()
    selected = filter_by_state(operations, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if _ask_yes_no("Отсортировать операции по дате? Да/Нет: "):
        ascending = _ask_sort_order()
        selected = sort_by_date(selected, reverse=not ascending)

    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет: "):
        selected = [operation for operation in selected if _is_ruble_transaction(operation)]

    if _ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "):
        search = input("Введите слово или фразу для поиска: ").strip()
        selected = process_bank_search(selected, search)

    print("Распечатываю итоговый список транзакций...")
    if not selected:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(selected)}\n")
    print("\n\n".join(format_operation(operation) for operation in selected))


def format_operation(operation: Operation) -> str:
    """Подготовить одну банковскую операцию для вывода в консоль."""
    date_text = _format_date(operation.get("date", ""))
    description = str(operation.get("description", "Операция без описания"))
    lines = [f"{date_text} {description}".strip()]

    source = operation.get("from")
    destination = operation.get("to")
    if source and destination:
        lines.append(f"{mask_account_card(str(source))} -> {mask_account_card(str(destination))}")
    elif source:
        lines.append(mask_account_card(str(source)))
    elif destination:
        lines.append(mask_account_card(str(destination)))

    amount, currency = _get_amount_and_currency(operation)
    if amount:
        lines.append(f"Сумма: {amount} {currency}".rstrip())
    return "\n".join(lines)


def _ask_file_type() -> str:
    """Запросить номер поддерживаемого формата файла."""
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice in FILE_OPTIONS:
            return choice
        print("Неверный пункт меню. Введите 1, 2 или 3.")


def _ask_status() -> str:
    """Запрашивать статус, пока пользователь не введёт допустимый."""
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        entered_status = input("Статус: ").strip()
        status = entered_status.upper()
        if status in VALID_STATUSES:
            return status
        print(f'Статус операции "{entered_status}" недоступен.')


def _ask_yes_no(question: str) -> bool:
    """Запросить ответ «да» или «нет», повторяя вопрос при ошибке."""
    while True:
        answer = input(question).strip().casefold()
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print("Пожалуйста, ответьте «Да» или «Нет».")


def _ask_sort_order() -> bool:
    """Вернуть True для сортировки по возрастанию, иначе по убыванию."""
    while True:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().casefold()
        if order in {"по возрастанию", "возрастанию", "по возрастанию даты", "asc", "ascending"}:
            return True
        if order in {"по убыванию", "убыванию", "по убыванию даты", "desc", "descending"}:
            return False
        print("Введите «по возрастанию» или «по убыванию».")


def _is_ruble_transaction(operation: Operation) -> bool:
    """Проверить, что валюта операции — российский рубль."""
    operation_amount = operation.get("operationAmount", {})
    if not isinstance(operation_amount, dict):
        return False
    currency = operation_amount.get("currency", {})
    if not isinstance(currency, dict):
        return False
    code = str(currency.get("code", "")).upper()
    name = str(currency.get("name", "")).strip().casefold()
    return code in {"RUB", "RUR"} or name in {"руб", "руб.", "рубль", "рублей", "рубля"}


def _get_amount_and_currency(operation: Operation) -> tuple[str, str]:
    """Получить сумму и обозначение валюты из операции."""
    operation_amount = operation.get("operationAmount", {})
    if not isinstance(operation_amount, dict):
        operation_amount = {}
    amount_value = operation_amount.get("amount", operation.get("amount", ""))
    currency = operation_amount.get("currency", {})
    if not isinstance(currency, dict):
        currency = {}
    currency_name = str(currency.get("name") or currency.get("code") or operation.get("currency_name", ""))
    if currency_name.upper() in {"RUB", "RUR"}:
        currency_name = "руб."
    return _format_amount(amount_value), currency_name


def _format_amount(amount: Any) -> str:
    """Отформатировать сумму без лишних нулей после десятичной точки."""
    if amount in (None, ""):
        return ""
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return str(amount)
    normalized = value.normalize()
    return format(normalized, "f")


def _format_date(value: Any) -> str:
    """Преобразовать дату операции в формат ДД.ММ.ГГГГ."""
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    if not value:
        return ""

    date_text = str(value).strip()
    try:
        parsed = datetime.fromisoformat(date_text.replace("Z", "+00:00"))
    except ValueError:
        return date_text
    return parsed.strftime("%d.%m.%Y")
