import sys, io
import numpy as np

# Устанавливаем корректную кодировку для вывода в консоль
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Параметры Варианта 3
N_QUARTERS = 3
Z_START = 20.0

# Жестко заданная сетка состояний X по условию задачи
X_GRID = np.array([0.0, 5.0, 10.0, 15.0, 20.0])
# Шаг изменения управления Y
DELTA_Y = 3.0


def g(Y):
    """Доход от сферы A"""
    return 6 * Y + 0.15 * (Y ** 2)


def h(X_minus_Y):
    """Доход от сферы B"""
    return 5 * X_minus_Y + 0.1 * (X_minus_Y ** 2)


def get_next_resource(Y, X):
    """Уравнение возврата ресурса: alpha*Y + beta*(X-Y)"""
    alpha = 0.4
    beta = 0.6
    return alpha * Y + beta * (X - Y)


def solve_task5():
    # Таблицы Беллмана: строки - шаги k (от 0 до N_QUARTERS-1), столбцы - элементы X_GRID
    F_tables = np.zeros((N_QUARTERS, len(X_GRID)))
    Y_tables = np.zeros((N_QUARTERS, len(X_GRID)))

    # Шаг 1 (Базовый случай)
    for i, X in enumerate(X_GRID):
        best_f = float('-inf')
        best_y = 0.0
        # Перебираем управления Y от 0 до X с шагом DELTA_Y
        for Y in np.arange(0.0, X + 1e-5, DELTA_Y):
            f_val = g(Y) + h(X - Y)
            if f_val > best_f:
                best_f = f_val
                best_y = Y
        F_tables[0, i] = best_f
        Y_tables[0, i] = best_y

    # Шаги 2 и 3 (Рекуррентный этап)
    for k in range(1, N_QUARTERS):
        for i, X in enumerate(X_GRID):
            best_f = float('-inf')
            best_y = 0.0
            for Y in np.arange(0.0, X + 1e-5, DELTA_Y):
                # Текущий доход от распределения
                immediate_income = g(Y) + h(X - Y)

                # Остаток ресурса на следующий квартал
                X_next = get_next_resource(Y, X)

                # Интерполируем ожидаемый доход будущего периода по сетке X_GRID
                future_income = np.interp(X_next, X_GRID, F_tables[k - 1])

                total_income = immediate_income + future_income
                if total_income > best_f:
                    best_f = total_income
                    best_y = Y
            F_tables[k, i] = best_f
            Y_tables[k, i] = best_y

    # Обратный ход (Восстановление оптимальной траектории)
    trajectory_X = [Z_START]
    trajectory_Y = []

    current_X = Z_START
    # Двигаемся от последнего шага (k = 2) обратно к первому (k = 0)
    for k in range(N_QUARTERS - 1, -1, -1):
        # Находим оптимальное управление для текущего состояния с помощью интерполяции политик
        opt_y = np.interp(current_X, X_GRID, Y_tables[k])
        # Ограничиваем сверху текущим X, чтобы избежать погрешностей интерполяции
        opt_y = min(opt_y, current_X)
        trajectory_Y.append(opt_y)

        # Вычисляем следующее состояние
        current_X = get_next_resource(opt_y, current_X)
        trajectory_X.append(current_X)

    trajectory_Y.reverse()

    return F_tables, Y_tables, trajectory_X, trajectory_Y


def print_task5(F_tables, Y_tables, traj_X, traj_Y):
    print("\n" + "=" * 64)
    print("ЗАДАЧА 5: Динамическое распределение ресурсов (Вариант 3)")
    print("=" * 64)

    print("\nТаблица Беллмана (Максимальный доход F_k(X) и управление Y_k*(X)):")
    header = f"{'X':>5} |"
    for k in range(1, N_QUARTERS + 1):
        header += f"   F{k}(X)   Y{k}* |"
    print(header)
    print("—" * 55)

    for i, X in enumerate(X_GRID):
        row = f"{int(X):>5} |"
        for k in range(N_QUARTERS):
            row += f" {F_tables[k, i]:8.2f} {Y_tables[k, i]:4.1f} |"
        print(row)

    print(f"\nВосстановление оптимальной траектории из начального бюджета Z = {Z_START}:")
    print("—" * 104)
    for q in range(N_QUARTERS):
        x_curr = traj_X[q]
        y_opt = traj_Y[q]
        x_next = traj_X[q + 1]
        income = g(y_opt) + h(x_curr - y_opt)
        print(
            f"Квартал {q + 1}: Доступно X = {x_curr:5.2f} -> "
            f"В сферу A: Y* = {y_opt:4.2f}, В сферу B: {x_curr - y_opt:4.2f} | "
            f"Доход = {income:6.2f} | X_next = {x_next:5.2f}"
        )

    print("—" * 104)
    print(f"Максимальный суммарный доход за {N_QUARTERS} квартала: F3({int(Z_START)}) = {F_tables[-1, -1]:.4f}")


def main():
    F_tabs, Y_tabs, t_X, t_Y = solve_task5()
    print_task5(F_tabs, Y_tabs, t_X, t_Y)


if __name__ == '__main__':
    main()
