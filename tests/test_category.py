"""Тесты модели категории и общих счётчиков каталога."""

from src.category import Category
from src.product import Product


def test_category_saves_constructor_arguments() -> None:
    """Категория хранит имя, описание и переданный список товаров."""
    products = [Product("Кружка", "Керамическая", 350.0, 4)]

    category = Category("Посуда", "Для кухни", products)

    assert category.name == "Посуда"
    assert category.description == "Для кухни"
    assert category.products is products


def test_category_counts_one_category_and_all_its_products() -> None:
    """При создании категории счётчики увеличиваются на категорию и её товары."""
    products = [
        Product("Тетрадь", "В клетку", 90.0, 10),
        Product("Ручка", "Синяя", 45.0, 20),
    ]

    Category("Канцелярия", "Для учёбы", products)

    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_counters_accumulate_across_categories() -> None:
    """Общие счётчики аккумулируют значения при создании разных категорий."""
    first_product = Product("Книга", "Роман", 650.0, 3)
    second_products = [
        Product("Лампа", "Настольная", 1200.0, 2),
        Product("Свеча", "Ароматическая", 300.0, 6),
    ]

    Category("Книги", "Литература", [first_product])
    Category("Дом", "Товары для дома", second_products)

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_empty_category_increments_only_category_count() -> None:
    """Пустая категория увеличивает число категорий, но не число товаров."""
    Category("Пусто", "Пока нет товаров", [])

    assert Category.category_count == 1
    assert Category.product_count == 0
