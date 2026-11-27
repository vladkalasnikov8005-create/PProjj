"""Класс товара с защищённой ценой и фабричным методом."""

from __future__ import annotations

from typing import Any


class Product:
    """Товар с названием, описанием, ценой и количеством на складе."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Создать товар, инициализируя цену через публичный сеттер."""
        self.name = name
        self.description = description
        self.__price = 0.0
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Вернуть цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Установить положительную цену, запросив подтверждение при её снижении."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            confirmation = input("Цена снижается. Подтвердите изменение (y/n): ").strip().lower()
            if confirmation != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(
        cls: type[Product],
        product_data: dict[str, Any],
        products: list[Product] | None = None,
    ) -> Product:
        """Создать товар из словаря, при необходимости объединяя дубликат по имени.

        При совпадении имени количество добавляется к существующему товару,
        а его цена остаётся максимальной из старой и новой.
        """
        name = str(product_data["name"])
        description = str(product_data["description"])
        price = product_data["price"]
        quantity = product_data["quantity"]

        if products is not None:
            normalized_name = name.strip().casefold()
            for existing_product in products:
                if existing_product.name.strip().casefold() == normalized_name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)
