"""Класс категории товаров с приватным списком продуктов."""

from typing import ClassVar

from src.product import Product


class Category:
    """Категория с названием, описанием и приватным списком товаров."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(self, name: str, description: str, products: list[Product] | None = None) -> None:
        """Создать категорию и добавить начальный список товаров."""
        self.name = name
        self.description = description
        self.__products: list[Product] = []

        Category.category_count += 1
        if products is not None:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product) -> None:
        """Добавить товар в приватный список и увеличить общий счётчик."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Вернуть список товаров строкой в формате каталога."""
        return "".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
            for product in self.__products
        )
