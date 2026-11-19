"""Варіант 3. Арифметична прогресія як лінивий потік."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Iterator
from itertools import accumulate, count, islice, takewhile, tee
from operator import add
from typing import TypeVar

T = TypeVar("T")
Num = TypeVar("Num", int, float)


# --- універсальні утиліти ------------------------------------------------------
def take(n: int, it: Iterable[T]) -> list[T]:
    """Перші n елементів (n <= 0 -> порожній список). Матеріалізує лише n."""
    return list(islice(it, max(n, 0)))


def drop(n: int, it: Iterable[T]) -> Iterator[T]:
    """Ліниво пропускає перші n елементів."""
    return islice(it, max(n, 0), None)


def sliding_window(it: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    """Ковзні вікна розміру k; у пам'яті тримається лише k елементів."""
    if k <= 0:
        raise ValueError("window size must be positive")
    window: deque[T] = deque(maxlen=k)
    for x in it:
        window.append(x)
        if len(window) == k:
            yield tuple(window)


# --- джерела потоків ---------------------------------------------------------
def arithmetic(start: Num, step: Num) -> Iterator[Num]:
    """Нескінченна арифметична прогресія a_n = start + n*step (itertools.count)."""
    return count(start, step)


def arithmetic_gen(start: int, step: int) -> Iterator[int]:
    """Те саме, але власним генератором з yield."""
    x = start
    while True:
        yield x
        x += step


def until_limit(limit: Num, it: Iterable[Num], step_sign: int = 1) -> Iterator[Num]:
    """Брати елементи, поки не перейдено межу (для спадної прогресії step_sign=-1)."""
    if step_sign >= 0:
        return takewhile(lambda x: x <= limit, it)
    return takewhile(lambda x: x >= limit, it)


def prefix_sums(it: Iterable[Num]) -> Iterator[Num]:
    """Префіксні (накопичувальні) суми: S_1, S_2, ..."""
    return accumulate(it, add)


def window_sums(it: Iterable[int], k: int) -> Iterator[int]:
    return (sum(w) for w in sliding_window(it, k))


def progression_pipeline(
    start: int, step: int, *, limit: int, skip: int
) -> Iterator[tuple[int, int]]:
    """Основне завдання варіанту:
    count(start, step) -> takewhile(<= limit) -> drop(skip) -> пари (a_n, S_n).
    Префіксні суми рахуються по елементах ПІСЛЯ пропуску.
    """
    sign = 1 if step >= 0 else -1
    body1, body2 = tee(drop(skip, until_limit(limit, arithmetic(start, step), sign)))
    return zip(body1, prefix_sums(body2), strict=True)


def nth_term(start: int, step: int, n: int) -> int:
    """Формула для перевірки: n-й член (з 0)."""
    return start + n * step


def sum_formula(start: int, step: int, n: int) -> int:
    """S_n = n*(2a + (n-1)d)/2 для перевірки accumulate."""
    return n * (2 * start + (n - 1) * step) // 2


def counted(it: Iterable[T], counter: Callable[[], None]) -> Iterator[T]:
    """Обгортка для тестів лінивості: викликає counter() на кожен ВИДАНИЙ елемент."""
    for x in it:
        counter()
        yield x
