from streams import (
    arithmetic,
    drop,
    prefix_sums,
    progression_pipeline,
    sliding_window,
    take,
    until_limit,
)


def main() -> None:
    print("Перші 10 членів 3, 7, 11, ...:", take(10, arithmetic(3, 4)))
    print("До межі 40:", list(until_limit(40, arithmetic(3, 4))))
    print("Пропустити 3, взяти 5:", take(5, drop(3, arithmetic(3, 4))))
    print("Префіксні суми (перші 6):", take(6, prefix_sums(arithmetic(1, 1))))
    print("Вікна k=3:", take(4, sliding_window(arithmetic(0, 5), 3)))
    print("Дробовий крок:", take(5, arithmetic(0.5, 0.25)))
    print("\nПрогресія start=2, step=3, limit=30, skip=2  ->  (a_n, S_n):")
    for a, s in progression_pipeline(2, 3, limit=30, skip=2):
        print(f"  a={a:>3}  S={s:>4}")
    print("Спадна 20, -4 до 0:", list(progression_pipeline(20, -4, limit=0, skip=0)))


if __name__ == "__main__":
    main()
