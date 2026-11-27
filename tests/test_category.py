"""Тесты модели категории, приватного списка и счётчиков."""

from src.category import Category
from src.product import Product


def test_category_saves_constructor_arguments_and_formats_products() -> None:
    """Категория хранит данные и возвращает товары в строковом формате."""
    products = [
        Product("Кружка", "Керамическая", 350.0, 4),
        Product("Тарелка", "Белая", 180, 6),
    ]

    category = Category("Посуда", "Для кухни", products)

    assert category.name == "Посуда"
    assert category.description == "Для кухни"
    assert category.products == (
        "Кружка, 350.0 руб. Остаток: 4 шт.\n"
        "Тарелка, 180 руб. Остаток: 6 шт.\n"
    )
    assert not hasattr(category, "__products")
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_add_product_returns_none_and_updates_private_list_and_counter() -> None:
    """Метод добавляет продукт, ничего не возвращает и увеличивает счётчик."""
    category = Category("Посуда", "Для кухни")
    product = Product("Кружка", "Керамическая", 350.0, 4)

    category.add_product(product)

    assert category.products == "Кружка, 350.0 руб. Остаток: 4 шт.\n"
    assert Category.product_count == 1


def test_empty_category_has_empty_products_string() -> None:
    """У пустой категории геттер возвращает пустую строку."""
    category = Category("Пустая", "Товаров пока нет")

    assert category.products == ""
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_category_counters_accumulate_across_categories_and_additions() -> None:
    """Счётчики учитывают начальные товары и товары, добавленные позже."""
    first_product = Product("Книга", "Роман", 650.0, 3)
    second_product = Product("Лампа", "Настольная", 1200.0, 2)
    first_category = Category("Книги", "Литература", [first_product])
    second_category = Category("Дом", "Товары для дома", [second_product])

    second_category.add_product(Product("Свеча", "Ароматическая", 300.0, 6))

    assert Category.category_count == 2
    assert Category.product_count == 3
    assert first_category.products == "Книга, 650.0 руб. Остаток: 3 шт.\n"
    assert second_category.products == (
        "Лампа, 1200.0 руб. Остаток: 2 шт.\n"
        "Свеча, 300.0 руб. Остаток: 6 шт.\n"
    )
