import sys, io
import numpy as np

# Устанавливаем корректную кодировку для вывода в консоль
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Исходные параметры Варианта 3
N_STEPS = 4
X_START = 15.0
STEP_H = 1

# Сетка состояний X от 0 до 15 включительно
X_GRID = np.arange(0, X_START + STEP_H, STEP_H)


def target_function(Y, X):
    """Текущие затраты на этапе: 5*Y^2 + (X-Y)^2"""
    return 5 * (Y ** 2) + ((X - Y) ** 2)


def get_next_state(Y, X):
    """Уравнение перехода к следующему состоянию: 0.2*Y + 0.8*(X-Y)"""
    return 0.2 * Y + 0.8 * (X - Y)


def solve_task2():
    # Таблицы для хранения значений функции Беллмана F и оптимального управления Y
    # Строки соответствуют шагам k (0 до N-1), столбцы - узлам сетки X
    F_tables = np.zeros((N_STEPS, len(X_GRID)))
    Y_tables = np.zeros((N_STEPS, len(X_GRID)))

    # Шаг 1 (Базовый случай)
    for i, X in enumerate(X_GRID):
        best_f = float('inf')
        best_y = 0.0
        # Перебираем возможные дискретные управления Y от 0 до X
        for Y in np.arange(0, X + STEP_H, STEP_H):
            f_val = target_function(Y, X)
            if f_val < best_f:
                best_f = f_val
                best_y = Y
        F_tables[0, i] = best_f
        Y_tables[0, i] = best_y

    # Шаги 2, 3, 4 (Рекуррентный этап)
    for k in range(1, N_STEPS):
        for i, X in enumerate(X_GRID):
            best_f = float('inf')
            best_y = 0.0
            for Y in np.arange(0, X + STEP_H, STEP_H):
                # Затраты на текущем шаге
                immediate_cost = target_function(Y, X)

                # Будущее состояние
                X_next = get_next_state(Y, X)

                # Линейная интерполяция значения Беллмана с предыдущего шага (k-1)
                future_cost = np.interp(X_next, X_GRID, F_tables[k - 1])

                total_cost = immediate_cost + future_cost
                if total_cost < best_f:
                    best_f = total_cost
                    best_y = Y
            F_tables[k, i] = best_f
            Y_tables[k, i] = best_y

    # Обратный ход (Восстановление оптимальной траектории)
    trajectory_X = [X_START]
    trajectory_Y = []

    current_X = X_START
    # Идем в обратном порядке от последнего шага к первому
    for k in range(N_STEPS - 1, -1, -1):
        # Находим оптимальное Y для текущего X методом интерполяции по таблице политик
        opt_y = np.interp(current_X, X_GRID, Y_tables[k])
        trajectory_Y.append(opt_y)

        # Переходим к следующему состоянию
        current_X = get_next_state(opt_y, current_X)
        trajectory_X.append(current_X)

    # Разворачиваем траектории, так как восстанавливали их с конца
    trajectory_Y.reverse()

    return F_tables, Y_tables, trajectory_X, trajectory_Y


def print_task2(F_tables, Y_tables, traj_X, traj_Y):
    print("\n" + "=" * 64)
    print("ЗАДАЧА 2: Нелинейное динамическое программирование (Вариант 3)")
    print("=" * 64)

    # Выводим таблицу результатов для состояний X
    print("\nТаблица Беллмана (Значения F_k(X) и оптимальные управления Y_k(X)):")
    header = f"{'X':>5} |"
    for k in range(1, N_STEPS + 1):
        header += f"   F{k}(X)   Y{k}* |"
    print(header)
    print("—" * 70)

    for i, X in enumerate(X_GRID):
        row = f"{int(X):>5} |"
        for k in range(N_STEPS):
            row += f" {F_tables[k, i]:8.2f} {Y_tables[k, i]:4.1f} |"
        print(row)

    print(f"\nВосстановление оптимальной траектории из начального состояния X = {X_START}:")
    print("—" * 70)
    for step in range(N_STEPS):
        x_curr = traj_X[step]
        y_opt = traj_Y[step]
        x_next = traj_X[step + 1]
        cost = target_function(y_opt, x_curr)
        print(
            f"Шаг {step + 1}: X = {x_curr:5.2f} -> "
            f"Выбираем Y* = {y_opt:4.2f} | "
            f"Затраты этапа = {cost:6.2f} | "
            f"X_next = {x_next:5.2f}"
        )

    print("—" * 70)
    print(f"Минимальные суммарные затраты F4({int(X_START)}) = {F_tables[-1, -1]:.4f}")


def main():
    F_tabs, Y_tabs, t_X, t_Y = solve_task2()
    print_task2(F_tabs, Y_tabs, t_X, t_Y)


if __name__ == '__main__':
    main()
