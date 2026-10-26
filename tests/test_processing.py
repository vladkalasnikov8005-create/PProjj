from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_uses_executed_by_default() -> None:
    operations = [
        {"state": "EXECUTED", "date": "2020-01-01"},
        {"state": "CANCELED", "date": "2020-01-02"},
    ]

    assert filter_by_state(operations) == [operations[0]]


def test_filter_by_state_accepts_another_state() -> None:
    operations = [
        {"state": "EXECUTED", "date": "2020-01-01"},
        {"state": "CANCELED", "date": "2020-01-02"},
    ]

    assert filter_by_state(operations, "CANCELED") == [operations[1]]


def test_sort_by_date_descending_by_default() -> None:
    older = {"date": "2020-01-01"}
    newer = {"date": "2020-01-02"}

    assert sort_by_date([older, newer]) == [newer, older]