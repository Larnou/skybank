import pytest

from src.processing import filter_by_state, sort_by_date

# Тестирование фильтрации списка словарей по заданному статусу state.
# Проверка работы функции при отсутствии словарей с указанным статусом state в списке.
# Параметризация тестов для различных возможных значений статуса state.


@pytest.mark.parametrize(
    "state_dictionary_result, state_key",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            "EXECUTED",
        ),
        (
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        ),
        ([{"id": 3412673132, "state": "DELAYED", "date": "2025-05-23T23:07:33.419441"}], "DELAYED"),
        ([], "POSTPONNED"),
    ],
)
def test_filter_by_state_values(state_dictionary_input, state_dictionary_result, state_key):
    assert filter_by_state(state_dictionary_input, state_key) == state_dictionary_result


# Тестирование сортировки списка словарей по датам в порядке убывания и возрастания.
# Проверка корректности сортировки при одинаковых датах.
# Тесты на работу функции с некорректными или нестандартными форматами дат.


@pytest.mark.parametrize(
    "state_dictionary_sortresult, sortway",
    [
        (
            [
                {"id": 3412673132, "state": "DELAYED", "date": "2025-05-23T23:07:33.419441"},
                {"id": 24112024, "state": "REORDERED", "date": "2025-05-23T23:07:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            True,
        ),
        (
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 3412673132, "state": "DELAYED", "date": "2025-05-23T23:07:33.419441"},
                {"id": 24112024, "state": "REORDERED", "date": "2025-05-23T23:07:33.419441"},
            ],
            False,
        ),
    ],
)
def test_sort_by_date_sortway(state_dictionary_input, state_dictionary_sortresult, sortway):
    assert sort_by_date(state_dictionary_input, sortway) == state_dictionary_sortresult


def test_sort_by_date_values(state_dictionary_input_incorrect):
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(state_dictionary_input_incorrect)
    assert str(exc_info.value) == 'Проверьте правильность введённых дат.\nФормат должен быть: "%Y-%m-%dT%H:%M:%S.f"'
