import sys, io
from scipy.optimize import linprog

# Устанавливаем корректную кодировку для вывода в консоль
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def solve_task1():
    # Целевая функция F (коэффициенты берем с минусом, так как linprog ищет минимум)
    c = [-9, -12, -10, -15, -8, -19]

    # Матрица коэффициентов левых частей ограничений (A_ub)
    A_ub = [
        [3, 4, 2, 5, 2, 6],  # 3x1 + 4x2 + 2x3 + 5x4 + 2x5 + 6x6 <= 220
        [2, 3, 1, 4, 1, 5],  # 2x1 + 3x2 + x3 + 4x4 + x5 + 5x6 <= 160
        [15, 20, 10, 25, 8, 30],  # 15x1 + 20x2 + 10x3 + 25x4 + 8x5 + 30x6 <= 850
        [-1, -1, -1, 0, 0, 0],  # -x1 - x2 - x3 <= -18 (изначально >= 18)
        [0, 0, 0, -1, -1, -1],  # -x4 - x5 - x6 <= -12 (изначально >= 12)
        [1, 0, 0, 0, 0, 1],  # x1 + x6 <= 14
    ]

    # Вектор правых частей ограничений (b_ub)
    b_ub = [220, 160, 850, -18, -12, 14]

    # Ограничения на переменные: xj >= 0
    bounds = [(0, None)] * 6

    # Решаем прямую задачу линейного программирования
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    # Получаем теневые цены (двойственные оценки)
    shadow_prices = res.ineqlin.marginals

    # Анализ чувствительности бюджета (+- 15% на второе ограничение)
    sensitivity = {}
    for pct in [-15, 0, 15]:
        b_s = list(b_ub)
        b_s[1] = 160 * (1 + pct / 100.0)  # Изменяем бюджет (160)
        r = linprog(c, A_ub=A_ub, b_ub=b_s, bounds=bounds, method="highs")
        sensitivity[pct] = round(-r.fun, 4) if r.success else None

    return res, shadow_prices, sensitivity


def print_task1(res, shadow_prices, sensitivity):
    var_names = [
        "x1 (модуль 1)",
        "x2 (модуль 2)",
        "x3 (модуль 3)",
        "x4 (модуль 4)",
        "x5 (модуль 5)",
        "x6 (модуль 6)",
    ]
    con_names = [
        "Ограничение 1 (<= 220)",
        "Ограничение 2 (<= 160)",
        "Ограничение 3 (<= 850)",
        "Ограничение 4 (x1+x2+x3 >= 18)",
        "Ограничение 5 (x4+x5+x6 >= 12)",
        "Ограничение 6 (x1+x6 <= 14)",
    ]

    print("\n" + "=" * 64)
    print("ЗАДАЧА 1: Линейное программирование (Вариант 3)")
    print("=" * 64)
    print(f"\nОптимальная маржа: F* = {-res.fun:.4f}")
    print(f"Статус решения:    {res.message}\n")

    print("Оптимальный план выпуска:")
    for name, val in zip(var_names, res.x):
        print(f"  {name}: {val:.4f}")

    print("\nТеневые цены (двойственные оценки):")
    for cname, sp in zip(con_names, shadow_prices):
        # Если теневая цена больше нуля (с учетом погрешности), ресурс дефицитный
        sign = "дефицит" if abs(sp) > 1e-6 else "избыток"
        print(f"  [{sign:7s}] {cname}: {sp:.4f}")

    base = sensitivity[0]
    print("\nАнализ чувствительности (изменение второго ограничения на +-15%):")
    for pct, val in sensitivity.items():
        delta = val - base if val is not None else None
        print(f"  Изменение {pct:+3d}%  ->  F = {val:.4f}  (дельта = {delta:+.4f})")


def main():
    res1, sp1, sens1 = solve_task1()
    print_task1(res1, sp1, sens1)


if __name__ == '__main__':
    main()
