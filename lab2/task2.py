import math


def calculate_infinite_queue_smo(lambda_day, t_min, alpha_cost, n_queue):
    """
    Расчет характеристик многоканальной СМО с неограниченной очередью.
    lambda_day: число заявок в сутки
    t_min: время обслуживания одной заявки в минутах
    alpha_cost: весовой коэффициент затрат (alpha)
    n_queue: число заявок в очереди для расчета вероятности P(очередь <= n)
    """
    # Перевод в часовую размерность
    arrival_rate = lambda_day / 24.0  # lambda
    service_rate = 60.0 / t_min  # mu
    rho = arrival_rate / service_rate  # интенсивность нагрузки

    # Критическое условие: k должно быть строго больше rho
    k_min = math.floor(rho) + 1

    def get_metrics(k):
        # Сумма для состояний, когда каналы свободны или частично заняты (от 0 до k-1)
        sum_p = sum((rho ** i) / math.factorial(i) for i in range(k))
        # Добавляем хвост с учетом геометрической очереди
        denominator = sum_p + (rho ** k) / (math.factorial(k) * (1 - rho / k))
        p0 = 1.0 / denominator

        # Вероятность того, что все каналы заняты (выделенная вероятность для очереди)
        p_k = (rho ** k) / math.factorial(k) * p0

        # Средняя длина очереди (Lq)
        queue_length = p_k * (rho / k) / ((1 - rho / k) ** 2)
        # Среднее время ожидания в очереди (Wq)
        queue_wait_time = queue_length / arrival_rate

        # Среднее число заявок в системе (Ls)
        system_length = queue_length + rho
        # Среднее время пребывания в системе (Ws)
        total_time = queue_wait_time + (1.0 / service_rate)

        # Функция затрат (критерий оптимизации)
        cost = (k / arrival_rate) + alpha_cost * total_time

        return p0, queue_length, system_length, queue_wait_time, total_time, cost

    # 1. Расчет характеристик для k_min
    p0_min, Lq_min, Ls_min, Wq_min, Ws_min, cost_min = get_metrics(k_min)

    # 2. Поиск экономического оптимума k_opt
    best_k = k_min
    best_cost = cost_min

    # Проверяем разумный диапазон увеличения каналов (например, до k_min + 10)
    for k in range(k_min + 1, k_min + 11):
        _, _, _, _, _, current_cost = get_metrics(k)
        if current_cost < best_cost:
            best_cost = current_cost
            best_k = k

    # 3. Расчет вероятности того, что в очереди будет <= n заявок
    # Это значит, что всего в системе находится <= (k_min + n) заявок
    p_queue_le_n = 0.0
    for i in range(k_min + n_queue + 1):
        if i <= k_min:
            p_i = (rho ** i) / math.factorial(i) * p0_min
        else:
            p_i = (rho ** i) / (math.factorial(k_min) * (k_min ** (i - k_min))) * p0_min
        p_queue_le_n += p_i

    return {
        "rho": rho,
        "k_min": k_min,
        "k_opt": best_k,
        "p0_min": p0_min,
        "Lq_min": Lq_min,
        "Ls_min": Ls_min,
        "Wq_min": Wq_min,
        "Ws_min": Ws_min,
        "cost_min": cost_min,
        "cost_opt": best_cost,
        "n_queue": n_queue,
        "p_queue": p_queue_le_n
    }


def main():
    LAMBDA_DAY = 150
    T_MIN = 15
    ALPHA_COST = 8
    N_QUEUE = 2

    res = calculate_infinite_queue_smo(
        lambda_day=LAMBDA_DAY,
        t_min=T_MIN,
        alpha_cost=ALPHA_COST,
        n_queue=N_QUEUE
    )

    print(f"\n=== Результаты расчета задачи 2 ===")
    print(f"Интенсивность нагрузки (rho): {res['rho']:.5f}")
    print(f"Минимальное число каналов (k_min): {res['k_min']}")
    print(f"Оптимальное число каналов (k_opt): {res['k_opt']}")

    print(f"\n--- Характеристики при k_min ({res['k_min']} кан.) ---")
    print(f"Вероятность простоя (P0): {res['p0_min']:.5f}")
    print(f"Средняя длина очереди (Lq): {res['Lq_min']:.5f} заявок")
    print(f"Среднее число заявок в системе (Ls): {res['Ls_min']:.5f} заявок")
    print(f"Среднее время ожидания в очереди (Wq): {res['Wq_min']:.5f} ч. ({res['Wq_min'] * 60:.2f} мин.)")
    print(f"Среднее время в системе (Ws): {res['Ws_min']:.5f} ч. ({res['Ws_min'] * 60:.2f} мин.)")
    print(f"Экономические затраты (C_min): {res['cost_min']:.5f}")

    print(f"\n--- Оптимизация ---")
    print(f"Затраты при k_opt ({res['k_opt']} кан.): {res['cost_opt']:.5f}")
    print(f"Вероятность того, что в очереди не более {res['n_queue']} заявок: {res['p_queue']:.5f}")


if __name__ == '__main__':
    main()
