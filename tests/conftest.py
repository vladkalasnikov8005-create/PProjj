"""Общие фикстуры для изолированных тестов каталога."""

from collections.abc import Iterator

import pytest

from src.category import Category


@pytest.fixture(autouse=True)
def reset_category_counters() -> Iterator[None]:
    """Сбрасывать общие счётчики категорий до и после каждого теста."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0
