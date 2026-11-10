# Bank Widget

Проект для обработки данных о банковских операциях.

Модуль `src/processing.py` умеет:
- фильтровать операции по статусу (`filter_by_state`)
- сортировать операции по дате (`sort_by_date`)

Модуль `src/masks.py` маскирует номер карты и номер счёта.

Модуль `src/widget.py` маскирует карту/счёт в строке и приводит дату к виду ДД.ММ.ГГГГ.

Модуль `src/generators.py` работает с транзакциями через генераторы:
- фильтр по валюте (`filter_by_currency`)
- описания операций (`transaction_descriptions`)
- номера карт (`card_number_generator`)

## Требования

- Python 3.12 или новее
- Poetry

Если Poetry ещё нет:

```bash
pip install poetry
```

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/vladkalasnikov8005-create/PProjj.git
cd PProjj
```

2. Установить все зависимости из `pyproject.toml` и `poetry.lock`:

```bash
poetry install
```

Ставятся:

- зависимости проекта
- pytest
- flake8
- mypy
- black
- isort

3. Активировать окружение:

```bash
poetry shell
```

Если `poetry shell` не работает, команды можно запускать через `poetry run`.

## Линтеры

```bash
poetry run flake8 .
poetry run mypy src tests
```

Настройки лежат в `.flake8` и в `pyproject.toml` (black, isort, mypy).

Форматирование:

```bash
poetry run black .
poetry run isort .
```

## Тесты

Нужны `pytest` и `pytest-cov` (ставятся через `poetry install`).

Запуск тестов:

```bash
poetry run pytest
```

Покрытие и HTML-отчёт (папка `htmlcov/`):

```bash
poetry run pytest --cov=src --cov-report=html --cov-report=term
```

Отчёт открывается файлом `htmlcov/index.html`. Покрытие должно быть не меньше 80%.

Тесты лежат отдельно по модулям:

- `tests/test_masks.py`
- `tests/test_widget.py`
- `tests/test_processing.py`
- `tests/test_generators.py`
- `tests/conftest.py` — фикстуры

## Использование

### filter_by_state

Принимает список словарей и необязательный параметр `state` (по умолчанию `"EXECUTED"`).
Возвращает новый список только с нужным статусом.

```python
from src.processing import filter_by_state

data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(filter_by_state(data))
print(filter_by_state(data, "CANCELED"))
```

### sort_by_date

Принимает список словарей и необязательный параметр `reverse` (по умолчанию `True` — сначала новые даты).
Возвращает новый список, отсортированный по ключу `date`.

```python
from src.processing import sort_by_date

print(sort_by_date(data))
print(sort_by_date(data, reverse=False))
```

### filter_by_currency

Принимает список транзакций и код валюты. Возвращает итератор только с этой валютой.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
```

### transaction_descriptions

Генератор описаний операций.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
```

### card_number_generator

Генератор номеров карт в формате `XXXX XXXX XXXX XXXX`.
Принимает `start` и `stop`.

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

Вывод:

```
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

## Структура проекта

- `src/processing.py` — фильтрация и сортировка операций
- `src/masks.py` — маски карты и счёта
- `src/widget.py` — маскировка карты/счёта в строке и дата
- `src/generators.py` — генераторы по транзакциям и номерам карт
- `tests/` — тесты
- `htmlcov/` — HTML-отчёт покрытия
- `pyproject.toml` — зависимости и настройки
- `.flake8` — настройки flake8
