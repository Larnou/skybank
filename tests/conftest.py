import pytest


@pytest.fixture
def state_dictionary_input():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 3412673132, "state": "DELAYED", "date": "2025-05-23T23:07:33.419441"},
        {"id": 24112024, "state": "REORDERED", "date": "2025-05-23T23:07:33.419441"},
    ]


@pytest.fixture
def state_dictionary_input_incorrect():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2021-11-24 04:26:18.914013"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "05-2024-04T12:26:18"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 3412673132, "state": "DELAYED", "date": "2025-05-23T23:07:33.419441"},
        {"id": 24112024, "state": "REORDERED", "date": "05-2024-04"},
    ]
