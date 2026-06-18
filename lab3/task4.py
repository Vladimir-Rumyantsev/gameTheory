import sys, io
import numpy as np

# Устанавливаем корректную кодировку для вывода в консоль
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Параметры Варианта 3
N_YEARS = 6
T_MAX = 6
START_AGE = 3


def R(t):
    """Функция прибыли в зависимости от возраста t"""
    return 20 - t


def C(t):
    """Функция затрат на замену оборудования возраста t"""
    return 3 + 4 * t


def solve_task4():
    # Таблицы Беллмана: строки - шаги k (оставшиеся годы от 1 до N_YEARS),
    # столбцы - текущий возраст t (от 0 до T_MAX)
    # Используем N_YEARS + 1 для удобства индексации по шагам
    F_table = np.zeros((N_YEARS + 1, T_MAX + 1))
    # Таблица решений: 1 - Продолжить (Keep), 0 - Заменить (Replace)
    Decision_table = np.zeros((N_YEARS + 1, T_MAX + 1), dtype=int)

    # Прямой ход ДП (Заполнение таблиц от k=1 до N_YEARS)
    for k in range(1, N_YEARS + 1):
        for t in range(0, T_MAX + 1):
            # Вариант 1: Продолжить эксплуатацию
            # Если возраст выходит за T_MAX, продолжать нельзя (ставим -inf)
            if t + 1 <= T_MAX:
                keep_val = R(t) + F_table[k - 1, t + 1]
            else:
                keep_val = float('-inf')

            # Вариант 2: Заменить оборудование
            replace_val = R(0) - C(t) + F_table[k - 1, 1]

            # Выбираем максимум
            if keep_val >= replace_val:
                F_table[k, t] = keep_val
                Decision_table[k, t] = 1  # Keep
            else:
                F_table[k, t] = replace_val
                Decision_table[k, t] = 0  # Replace

    # Обратный ход (Восстановление оптимальной политики по годам от 1 до N)
    policy_history = []
    current_age = START_AGE

    # Идем по реальным годам хронологически: от 1-го года до N-го
    # Для хронологического года `year`, количество оставшихся лет k = N_YEARS - year + 1
    for year in range(1, N_YEARS + 1):
        k_left = N_YEARS - year + 1
        decision = Decision_table[k_left, current_age]

        age_before = current_age
        if decision == 1:
            action = "Продолжить работу"
            profit = R(current_age)
            current_age += 1
        else:
            action = "Заменить"
            profit = R(0) - C(age_before)
            current_age = 1

        policy_history.append({
            'year': year,
            'age': age_before,
            'action': action,
            'profit': profit,
            'next_age': current_age
        })

    return F_table, Decision_table, policy_history


def print_task4(F_table, policy_history):
    print("\n" + "=" * 64)
    print("ЗАДАЧА 4: Оптимальная политика замены оборудования (Вариант 3)")
    print("=" * 64)

    print("\nТаблица Беллмана F_k(t) (Максимальная прибыль при оставшихся k годах):")
    header = f"{'Возраст t':^10} |"
    for k in range(1, N_YEARS + 1):
        header += f"   k = {k}   |"
    print(header)
    print("—" * 84)
    for t in range(T_MAX + 1):
        row = f"{t:^10} |"
        for k in range(1, N_YEARS + 1):
            val = F_table[k, t]
            row += f" {val:9.1f} |" if val != float('-inf') else f" {'-INF':>9} |"
        print(row)

    print("\nВосстановление оптимального жизненного цикла фреймворка:")
    print(f"Начальные условия: Год 1, Начальный возраст t = {START_AGE}")
    print("—" * 94)
    total_net_profit = 0
    for h in policy_history:
        print(
            f"Год {h['year']}: Возраст t = {h['age']} -> "
            f"Решение: {h['action']:18s} | "
            f"Прибыль этапа = {h['profit']:4.1f} | "
            f"Новый возраст = {h['next_age']}"
        )
        total_net_profit += h['profit']
    print("—" * 94)
    print(f"Максимальная суммарная прибыль за {N_YEARS} лет: {total_net_profit:.1f}")


def main():
    F_tab, Dec_tab, history = solve_task4()
    print_task4(F_tab, history)


if __name__ == '__main__':
    main()
