"""Фикстуры с тестовыми данными."""

from typing import Any

import pytest


@pytest.fixture
def sample_operations() -> list[dict[str, Any]]:
    """Список операций с разными статусами и датами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "PENDING", "date": "2018-10-14T08:21:33.419441"},
        {"id": 5, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def card_number() -> str:
    """Номер карты стандартной длины."""
    return "7000792289606361"


@pytest.fixture
def account_number() -> str:
    """Номер счёта."""
    return "73654108430135874305"
