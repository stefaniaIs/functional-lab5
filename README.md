# Лабораторна робота №5 — Ліниві обчислення: генератори та itertools

**Варіант 3. Арифметична прогресія.** Іщенко Стефанія, ФеП-22.

Вхід: `start`, `step` і нескінченний потік `itertools.count(start, step)`.
Завдання: відібрати елементи до межі (`takewhile`), пропустити перші k (`drop`),
обчислити префіксні суми (`accumulate`).

## `streams.py`
- `take(n, it)`, `drop(n, it)` (через `islice`), `sliding_window(it, k)` (через `deque(maxlen=k)`, власний генератор з `yield`);
- `arithmetic(start, step)` — `count`; `arithmetic_gen` — те саме власним генератором;
- `until_limit(limit, it)` — `takewhile` (підтримує й спадну прогресію);
- `prefix_sums(it)` — `accumulate(it, operator.add)`;
- `window_sums`, `progression_pipeline(start, step, limit=, skip=)` → ліниві пари `(aₙ, Sₙ)` (через `tee` + `zip`);
- `nth_term`, `sum_formula` — формули для перевірки; `counted` — обгортка для тесту лінивості.

itertools: `count`, `islice`, `takewhile`, `accumulate`, `tee`.
Нескінченний потік ніде не матеріалізується повністю — лише через `take`/`takewhile`.

## Тести (`tests/test_streams.py`)
Перші члени і формула `aₙ = a + n·d`, префіксні суми проти `Sₙ = n(2a+(n−1)d)/2`,
крайові випадки (порожнє джерело, `n=0`, `n<0`, `k>довжини`, `k<=0` → `ValueError`),
спадна прогресія, **тест лінивості** (з нескінченного потоку обчислено рівно 5 елементів:
2 пропущено + 3 взято), вичерпання генератора.

## Запуск
```bash
pip install -r requirements.txt
pytest -q
mypy . && black --check . && ruff check .
python main.py
```
