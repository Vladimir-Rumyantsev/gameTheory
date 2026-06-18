import math


def calculate_impatient_smo(lambda_m, t_min, k_channels, omega_patience, C_cost, eps=0.01):
    """
    Расчет СМО с нетерпеливыми заявками (ограниченное время ожидания).
    lambda_m: интенсивность входящего потока (заявки в минуту)
    t_min: время обслуживания (в минутах)
    k_channels: количество каналов (k)
    omega_patience: среднее время терпения в очереди (минуты)
    C_cost: убыток от ухода одной заявки
    eps: точность расчета бесконечных рядов
    """
    arrival_rate = lambda_m  # lambda
    service_rate = 1.0 / t_min  # mu
    patience_rate = 1.0 / omega_patience  # nu
    rho = arrival_rate / service_rate

    # Считаем P0 с бесконечным рядом
    # Базовая часть (до k включительно)
    sum_base = sum((rho ** i) / math.factorial(i) for i in range(k_channels + 1))

    # Хвост очереди (бесконечный ряд)
    sum_tail = 0.0
    i = 1
    prefix = (rho ** k_channels) / math.factorial(k_channels)

    while True:
        # Произведение в знаменателе: (k*mu + 1*nu) * (k*mu + 2*nu) * ...
        denominator_product = math.prod((k_channels * service_rate + j * patience_rate) for j in range(1, i + 1))
        current_term = (arrival_rate ** i) / denominator_product
        sum_tail += current_term

        # Если очередной член ряда пренебрежимо мал, останавливаемся
        if prefix * current_term < eps * 0.001:
            break
        i += 1

    p0 = 1.0 / (sum_base + prefix * sum_tail)

    # Считаем средние характеристики (Lq и k_busy) через распределение вероятностей
    # Будем вычислять вероятности состояний Pm, пока они вносят вклад
    probabilities = [p0]

    # Вероятности до k
    for m in range(1, k_channels + 1):
        pm = ((rho ** m) / math.factorial(m)) * p0
        probabilities.append(pm)

    # Вероятности для m > k (очередь)
    m = k_channels + 1
    while True:
        i = m - k_channels
        denominator_product = math.prod((k_channels * service_rate + j * patience_rate) for j in range(1, i + 1))
        pm = prefix * ((arrival_rate ** i) / denominator_product) * p0
        probabilities.append(pm)
        if pm < eps * 0.0001 and m > 100:  # Гарантия сходимости
            break
        m += 1

    # Среднее число занятых каналов
    k_busy = 0.0
    for m in range(len(probabilities)):
        if m < k_channels:
            k_busy += m * probabilities[m]
        else:
            k_busy += k_channels * probabilities[m]

    # Средняя длина очереди Lq
    Lq = 0.0
    for m in range(k_channels + 1, len(probabilities)):
        Lq += (m - k_channels) * probabilities[m]

    # Полное число заявок в системе Ls
    Ls = Lq + k_busy

    # Вероятности исходов
    p_refusal = (patience_rate * Lq) / arrival_rate  # Вероятность ухода по нетерпению
    p_service = 1.0 - p_refusal  # Вероятность обслуживания

    # Временные характеристики (в минутах)
    Wq = Lq / arrival_rate
    Ws = Wq + (p_service / service_rate)
    W_obs = Ws - Wq

    # Экономические потери в минуту
    loss_per_minute = C_cost * arrival_rate * p_refusal

    return {
        "rho": rho,
        "p0": p0,
        "p_service": p_service,
        "p_refusal": p_refusal,
        "Lq": Lq,
        "k_busy": k_busy,
        "Ls": Ls,
        "Wq": Wq,
        "W_obs": W_obs,
        "Ws": Ws,
        "loss_per_min": loss_per_minute
    }


def main():
    LAMBDA_M = 0.4
    T_MIN = 4
    K_CHANNELS = 2
    OMEGA_PATIENCE = 20
    C_COST = 350
    EPS = 0.01

    res = calculate_impatient_smo(
        lambda_m=LAMBDA_M,
        t_min=T_MIN,
        k_channels=K_CHANNELS,
        omega_patience=OMEGA_PATIENCE,
        C_cost=C_COST,
        eps=EPS
    )

    print(f"\n=== Результаты расчета задачи 4 ===")
    print(f"Интенсивность нагрузки (rho): {res['rho']:.5f}")
    print(f"Предельная вероятность простоя (P0): {res['p0']:.5f}")
    print(f"Вероятность обслуживания (P_обсл): {res['p_service']:.5f}")
    print(f"Вероятность ухода по нетерпению (P_уход): {res['p_refusal']:.5f}")
    print(f"Среднее число заявок в очереди (Lq): {res['Lq']:.5f}")
    print(f"Среднее число занятых каналов (k_зан): {res['k_busy']:.5f}")
    print(f"Среднее число заявок в системе (Ls): {res['Ls']:.5f}")
    print(f"Среднее время ожидания в очереди (Wq): {res['Wq']:.5f} мин.")
    print(f"Среднее время под обслуживанием (W_обсл): {res['W_obs']:.5f} мин.")
    print(f"Среднее время пребывания в системе (Ws): {res['Ws']:.5f} мин.")
    print(f"Средние потери дохода: {res['loss_per_min']:.5f} у.е./мин")


if __name__ == '__main__':
    main()
