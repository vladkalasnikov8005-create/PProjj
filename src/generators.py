"""Модуль с генераторами для обработки транзакций."""

from collections.abc import Iterator
from typing import Any

Transaction = dict[str, Any]


def filter_by_currency(
    transactions: list[Transaction],
    currency: str,
) -> Iterator[Transaction]:
    """Вернуть итератор транзакций с заданной валютой."""
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        code = operation_amount.get("currency", {}).get("code")
        if code == currency:
            yield transaction


def transaction_descriptions(transactions: list[Transaction]) -> Iterator[str]:
    """Вернуть описание каждой операции по очереди."""
    for transaction in transactions:
        yield str(transaction.get("description", ""))


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Сгенерировать номера карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, stop + 1):
        digits = f"{number:016d}"
        yield f"{digits[:4]} {digits[4:8]} {digits[8:12]} {digits[12:]}"
