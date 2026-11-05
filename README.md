# Bank Widget

Проект для обработки данных о банковских операциях.

## Установка

Нужны Python 3.14 и Poetry.

1. Клонировать репозиторий:

```bash
git clone https://github.com/vladkalasnikov8005-create/PProjj.git
cd PProjj
```

2. Установить зависимости:

```bash
poetry install
```

Ставятся зависимости проекта, pytest и линтеры (flake8, mypy, black, isort).

3. Активировать окружение:

```bash
poetry shell
```

## Линтеры

```bash
flake8 .
mypy src
```

## Тесты

```bash
pytest
```

## Использование

Фильтр по статусу (по умолчанию EXECUTED):

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

Сортировка по дате (сначала новые):

```python
from src.processing import sort_by_date

print(sort_by_date(data))
print(sort_by_date(data, reverse=False))
```
