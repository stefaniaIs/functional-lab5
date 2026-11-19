from itertools import count

import pytest

from streams import (
    arithmetic,
    arithmetic_gen,
    counted,
    drop,
    nth_term,
    prefix_sums,
    progression_pipeline,
    sliding_window,
    sum_formula,
    take,
    until_limit,
    window_sums,
)


def test_first_terms() -> None:
    assert take(5, arithmetic(3, 4)) == [3, 7, 11, 15, 19]
    assert take(5, arithmetic_gen(3, 4)) == [3, 7, 11, 15, 19]
    assert all(
        x == nth_term(3, 4, i) for i, x in enumerate(take(100, arithmetic(3, 4)))
    )


def test_take_drop_edge_cases() -> None:
    assert take(0, arithmetic(1, 1)) == []
    assert take(-3, arithmetic(1, 1)) == []
    assert take(5, []) == []
    assert take(5, [1, 2]) == [1, 2]
    assert list(drop(5, [1, 2])) == []
    assert take(3, drop(-1, arithmetic(1, 1))) == [1, 2, 3]
    assert take(3, drop(4, arithmetic(0, 2))) == [8, 10, 12]


def test_takewhile_limit() -> None:
    assert list(until_limit(20, arithmetic(2, 5))) == [2, 7, 12, 17]
    assert list(until_limit(1, arithmetic(5, 1))) == []
    assert list(until_limit(0, arithmetic(10, -3), step_sign=-1)) == [10, 7, 4, 1]


def test_prefix_sums_match_formula() -> None:
    sums = take(50, prefix_sums(arithmetic(3, 4)))
    assert sums == [sum_formula(3, 4, n) for n in range(1, 51)]
    assert list(prefix_sums([])) == []


def test_pipeline() -> None:
    # 2,5,8,11,14,17,20,23,26,29 -> skip 2 -> 8,11,14,...
    res = list(progression_pipeline(2, 3, limit=30, skip=2))
    assert res[:3] == [(8, 8), (11, 19), (14, 33)]
    assert res[-1] == (29, 148)
    assert list(progression_pipeline(2, 3, limit=30, skip=100)) == []
    assert list(progression_pipeline(20, -4, limit=0, skip=0))[-1] == (0, 60)


def test_sliding_window() -> None:
    assert list(sliding_window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    assert list(sliding_window([1, 2], 5)) == []  # k > довжини
    assert list(sliding_window([], 1)) == []
    assert take(3, window_sums(arithmetic(1, 1), 3)) == [6, 9, 12]
    with pytest.raises(ValueError):
        list(sliding_window([1, 2], 0))


def test_laziness_only_requested_elements_computed() -> None:
    produced = {"n": 0}

    def tick() -> None:
        produced["n"] += 1

    stream = counted(count(0, 3), tick)  # нескінченний
    pipeline = prefix_sums(drop(2, until_limit(10**9, stream)))
    assert produced["n"] == 0  # ще нічого не обчислено
    assert take(3, pipeline) == [6, 15, 27]
    assert produced["n"] == 5  # 2 пропущено + 3 взято, не більше


def test_generator_exhausts() -> None:
    g = until_limit(5, arithmetic(1, 2))
    assert list(g) == [1, 3, 5]
    assert list(g) == []  # генератор вичерпано
