"""Класс категории товаров интернет-магазина."""

from typing import ClassVar

from src.product import Product


class Category:
    """Категория с описанием и списком входящих в неё товаров."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        """Создать категорию и обновить общие счётчики каталога."""
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)
