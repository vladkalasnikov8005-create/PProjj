"""Тесты модели товара."""

from src.product import Product


def test_product_saves_all_constructor_arguments() -> None:
    """Поля товара должны совпадать со значениями конструктора."""
    product = Product("Чай", "Листовой чёрный чай", 450.5, 12)

    assert product.name == "Чай"
    assert product.description == "Листовой чёрный чай"
    assert product.price == 450.5
    assert product.quantity == 12
