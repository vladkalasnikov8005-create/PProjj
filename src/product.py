"""Класс товара для модели интернет-магазина."""


class Product:
    """Товар с названием, описанием, ценой и количеством на складе."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Создать товар и сохранить переданные характеристики."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
