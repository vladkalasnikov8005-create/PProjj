"""Тесты модели товара, цены и фабричного метода."""

import pytest

from src.product import Product


def test_product_saves_constructor_arguments() -> None:
    """Поля товара совпадают со значениями, переданными конструктору."""
    product = Product("Чай", "Листовой чёрный чай", 450.5, 12)

    assert product.name == "Чай"
    assert product.description == "Листовой чёрный чай"
    assert product.price == 450.5
    assert product.quantity == 12


def test_new_product_creates_product_from_dictionary() -> None:
    """Класс-метод создаёт товар на основе словаря."""
    product = Product.new_product(
        {
            "name": "Кофе",
            "description": "Зёрна арабики",
            "price": 790.0,
            "quantity": 8,
        }
    )

    assert isinstance(product, Product)
    assert product.name == "Кофе"
    assert product.description == "Зёрна арабики"
    assert product.price == 790.0
    assert product.quantity == 8


def test_new_product_merges_duplicate_and_keeps_higher_price() -> None:
    """Дубликат по имени увеличивает количество и обновляет цену вверх."""
    existing_product = Product("Кофе", "Арабика", 700.0, 5)
    products = [existing_product]

    result = Product.new_product(
        {
            "name": " кофе ",
            "description": "Новая поставка",
            "price": 850.0,
            "quantity": 3,
        },
        products,
    )

    assert result is existing_product
    assert existing_product.quantity == 8
    assert existing_product.price == 850.0
    assert len(products) == 1


def test_new_product_merges_duplicate_without_lowering_price() -> None:
    """При дубликате с меньшей ценой остаётся прежняя цена."""
    existing_product = Product("Кофе", "Арабика", 700.0, 5)

    result = Product.new_product(
        {
            "name": "Кофе",
            "description": "Новая поставка",
            "price": 650.0,
            "quantity": 2,
        },
        [existing_product],
    )

    assert result is existing_product
    assert existing_product.quantity == 7
    assert existing_product.price == 700.0


def test_positive_price_can_be_set() -> None:
    """Положительное значение цены сохраняется."""
    product = Product("Чай", "Чёрный", 450.0, 12)

    product.price = 500.0

    assert product.price == 500.0


@pytest.mark.parametrize("invalid_price", [0, -10.0])
def test_nonpositive_price_is_rejected(invalid_price: float, capsys: pytest.CaptureFixture[str]) -> None:
    """Нулевую и отрицательную цену нельзя сохранить."""
    product = Product("Чай", "Чёрный", 450.0, 12)

    product.price = invalid_price

    assert product.price == 450.0
    assert capsys.readouterr().out == "Цена не должна быть нулевая или отрицательная\n"


def test_price_reduction_can_be_declined(monkeypatch: pytest.MonkeyPatch) -> None:
    """Любой ответ, кроме y, отменяет снижение цены."""
    product = Product("Чай", "Чёрный", 450.0, 12)
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    product.price = 400.0

    assert product.price == 450.0


def test_price_reduction_is_applied_after_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ответ y подтверждает снижение цены."""
    product = Product("Чай", "Чёрный", 450.0, 12)
    monkeypatch.setattr("builtins.input", lambda _prompt: " Y ")

    product.price = 400.0

    assert product.price == 400.0
