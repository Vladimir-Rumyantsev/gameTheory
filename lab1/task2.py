import numpy as np
from scipy.optimize import linprog


def solve_security_stackelberg(budget=80):   # Общий доступный бюджет службы безопасности

    # 1. Формируем параметры инфраструктуры (5 критических узлов)
    # Названия узлов для наглядности отчёта
    node_names = [
        "Web-сервер (Узел 1)",
        "База данных пользователей (Узел 2)",
        "Шлюз оплаты (Узел 3)",
        "Почтовый сервер (Узел 4)",
        "Внутренняя wiki-система (Узел 5)"
    ]

    # Ценность узлов (потенциальный ущерб при компрометации)
    V = np.array([120, 250, 180, 90, 60])
    # Стоимость построения комплексной защиты на каждом узле
    C = np.array([25, 45, 35, 15, 10])

    # Вероятность пробития, если защита поставлена (низкая)
    P_def = np.array([0.15, 0.05, 0.10, 0.20, 0.25])
    # Вероятность пробития БЕЗ защиты (высокая)
    P_nodef = np.array([0.85, 0.95, 0.90, 0.75, 0.60])

    num_nodes = len(V)

    print("\n" + "=" * 64)
    print("ИСХОДНЫЕ ДАННЫЕ МОДЕЛИ БЕЗОПАСНОСТИ ШТАКЕЛЬБЕРГА:")
    for i in range(num_nodes):
        print(f" - {node_names[i]}: Ценность = {V[i]}, Стоимость защиты = {C[i]}")
    print(f"Доступный бюджет: {budget}")
    print("=" * 64)

    # 2. Сведение минимаксной задачи к стандартной задаче линейного программирования
    # Вектор переменных: [Z, x_1, x_2, ..., x_N], где Z - целевой максимальный ущерб
    # Мы хотим минимизировать Z, поэтому целевая функция: 1*Z + 0*x_1 + ... + 0*x_N
    c_vector = np.zeros(num_nodes + 1)
    c_vector[0] = 1.0  # Коэффициент перед Z

    # Ограничения: Ущерб_i(x_i) <= Z  =>  -Z + Ущерб_i(x_i) <= 0
    # Раскрываем Ущерб_i: V_i * (x_i * P_def_i + (1 - x_i) * P_nodef_i) <= Z
    # Переносим всё с x_i и Z влево: -Z + x_i * V_i * (P_def_i - P_nodef_i) <= -V_i * P_nodef_i
    A_ub = np.zeros((num_nodes, num_nodes + 1))
    b_ub = np.zeros(num_nodes)

    for i in range(num_nodes):
        A_ub[i, 0] = -1.0  # коэффициент при Z
        A_ub[i, i + 1] = V[i] * (P_def[i] - P_nodef[i])  # коэффициент при x_i
        b_ub[i] = -V[i] * P_nodef[i]  # свободный член

    # Добавляем бюджетное ограничение: 0*Z + C_1*x_1 + ... + C_N*x_N <= budget
    budget_constraint_row = np.zeros(num_nodes + 1)
    budget_constraint_row[1:] = C

    # Объединяем матрицы ограничений
    A_ub = np.vstack([A_ub, budget_constraint_row])
    b_ub = np.append(b_ub, budget)

    # Границы для переменных: Z >= 0, и 0 <= x_i <= 1
    variable_bounds = [(0, None)] + [(0, 1) for _ in range(num_nodes)]

    # 3. Решение задачи линейного программирования
    solution = linprog(c_vector, A_ub=A_ub, b_ub=b_ub, bounds=variable_bounds, method='highs')

    # 4. Вывод и интерпретация результатов
    if solution.success:
        optimal_max_damage = solution.x[0]
        optimal_protection = solution.x[1:]

        print("\nРЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ СТРАТЕГИИ ЗАЩИТЫ:")
        print(f"Гарантированный (минимаксный) ожидаемый ущерб системы: {optimal_max_damage:.2f}")
        print("\nОптимальное распределение ресурсов (вероятности/степень защиты):")

        for i in range(num_nodes):
            print(f" - {node_names[i]}: {optimal_protection[i] * 100:.1f}%")

        spent_budget = np.sum(optimal_protection * C)
        print(f"\nИспользованный бюджет: {spent_budget:.2f} из {budget}")

        # Рассчитаем финальные риски по каждому узлу, чтобы увидеть логику игры
        print("\nПроверка рисков по узлам (ожидаемый ущерб для хакера при атаке):")
        for i in range(num_nodes):
            node_damage = V[i] * (optimal_protection[i] * P_def[i] + (1 - optimal_protection[i]) * P_nodef[i])
            print(f" - При атаке на {node_names[i]}: {node_damage:.2f}")

    else:
        print("\nОшибка: Не удалось найти оптимальную стратегию защиты.")


def main(random_seed=42):
    np.random.seed(random_seed)   # Настройка воспроизводимости
    solve_security_stackelberg()


if __name__ == "__main__":
    main()
