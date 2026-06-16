import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


def fictitious_play(payoff_matrix, iterations=5000):
    """
    Реализация алгоритма Брауна-Робинсона (фиктивного разыгрывания).
    """
    num_rows, num_cols = payoff_matrix.shape

    # Счётчики выбора стратегий
    row_counts = np.zeros(num_rows)
    col_counts = np.zeros(num_cols)

    # Накопленные выигрыши/проигрыши
    accumulated_row_payoffs = np.zeros(num_rows)
    accumulated_col_payoffs = np.zeros(num_cols)

    lower_bounds = []
    upper_bounds = []

    # Начальный случайный выбор
    current_row = np.random.randint(num_rows)
    current_col = np.random.randint(num_cols)

    for t in range(1, iterations + 1):
        # Фиксируем выбор текущего раунда
        row_counts[current_row] += 1
        col_counts[current_col] += 1

        # Обновляем накопленные выигрыши
        accumulated_row_payoffs += payoff_matrix[:, current_col]
        accumulated_col_payoffs += payoff_matrix[current_row, :]

        # Вычисляем текущие границы цены игры
        current_lower = np.max(accumulated_row_payoffs) / t
        current_upper = np.min(accumulated_col_payoffs) / t

        lower_bounds.append(current_lower)
        upper_bounds.append(current_upper)

        # Игроки делают наилучший ответ на основе накопленной статистики
        current_row = np.argmax(accumulated_row_payoffs)
        current_col = np.argmin(accumulated_col_payoffs)

    # Преобразуем частоты в вероятности (смешанные стратегии)
    p_strategy = row_counts / iterations
    q_strategy = col_counts / iterations
    game_value_approx = (lower_bounds[-1] + upper_bounds[-1]) / 2.0

    return p_strategy, q_strategy, game_value_approx, lower_bounds, upper_bounds


def solve_linear_programming(payoff_matrix):
    """
    Точное решение матричной игры через сведение к задаче линейного программирования.
    """
    num_rows, num_cols = payoff_matrix.shape

    # Избавляемся от отрицательных элементов, смещая матрицу
    shift = payoff_matrix.min() - 1
    matrix_positive = payoff_matrix - shift if shift <= 0 else payoff_matrix
    shift_val = shift if shift <= 0 else 0

    # Оптимизация для Игрока 1 (максимизация выигрыша)
    # Переходим к задаче минимизации: c = [1, 1, ..., 1]
    c = np.ones(num_rows)
    A_ub = -matrix_positive.T
    b_ub = -np.ones(num_cols)

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

    if not res.success:
        raise ValueError("Не удалось решить задачу линейного программирования")

    game_value = (1.0 / res.fun) + shift_val
    p_optimal = res.x * (1.0 / res.fun)

    return p_optimal, game_value


def main(random_seed=42, n=12, m=12, iterations=5000):   # Размеры матрицы n > 10, m > 10

    # Настройка воспроизводимости
    np.random.seed(random_seed)

    A = np.random.randint(-100, 101, size=(n, m))

    print(f"\nСгенерирована платёжная матрица A ({n}x{m}):")
    print(A)

    # 1. Запуск итерационного метода
    p_fp, q_fp, val_fp, lb, ub = fictitious_play(A, iterations)

    # 2. Запуск точного метода линейного программирования
    p_lp, val_lp = solve_linear_programming(A)

    # Вывод результатов
    print("\n" + "=" * 64)
    print(f"РЕЗУЛЬТАТЫ МЕТОДА БРАУНА-РОБИНСОНА ({iterations} итераций):")
    print(f"Приближенная цена игры: {val_fp:.4f}")
    print(f"Смешанная стратегия Игрока 1 (первые 5 элементов): {p_fp[:5]}")

    print("\nРЕЗУЛЬТАТЫ ЛИНЕЙНОГО ПРОГРАММИРОВАНИЯ:")
    print(f"Точная цена игры (LP): {val_lp:.4f}")
    print(f"Разница между методами: {abs(val_fp - val_lp):.6f}")
    print("=" * 64)

    # Визуализация сходимости
    plt.figure(figsize=(11, 6))
    plt.plot(lb, label="Нижняя оценка цены ($v_{min}$)", color='#1f77b4', linewidth=1.2)
    plt.plot(ub, label="Верхняя оценка цены ($v_{max}$)", color='#d62728', linewidth=1.2)
    plt.axhline(val_lp, color='black', linestyle='--', label=f"Точная цена = {val_lp:.2f} (LP)")

    plt.title("График сходимости итерационного метода Брауна-Робинсона", fontsize=12, fontweight='bold')
    plt.xlabel("Итерация", fontsize=10)
    plt.ylabel("Цена игры", fontsize=10)
    plt.legend(loc="best")
    plt.grid(True, linestyle=':', alpha=0.6)

    # Сохраняем график
    plt.savefig('task1_convergence.png', dpi=300)
    print("\nГрафик успешно сохранен: 'lab1/task1_convergence.png'")


if __name__ == '__main__':
    main()
