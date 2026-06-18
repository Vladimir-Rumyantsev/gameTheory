import math


def calculate_limited_queue_smo(lambda_h, t_min, k_channels, n_max_queue, T_hours, C_cost):
    """
    Расчет характеристик многоканальной СМО с ограниченной очередью.
    lambda_h: интенсивность поступающего потока (заявок в час)
    t_min: время обслуживания (в минутах)
    k_channels: число каналов (k)
    n_max_queue: максимальная длина очереди (n)
    T_hours: рассматриваемый период работы системы (в часах)
    C_cost: стоимость упущенной выгоды от одной недополученной заявки (C)
    """
    arrival_rate = lambda_h
    service_rate = 60.0 / t_min
    rho = arrival_rate / service_rate

    # 1. Расчет вероятности простоя P0
    sum_k = sum((rho ** i) / math.factorial(i) for i in range(k_channels + 1))
    sum_n = sum((rho ** i) / (math.factorial(k_channels) * (k_channels ** (i - k_channels)))
                for i in range(k_channels + 1, k_channels + n_max_queue + 1))
    p0 = 1.0 / (sum_k + sum_n)

    # 2. Вероятность отказа и пропускная способность
    p_refusal = (rho ** (k_channels + n_max_queue)) / (math.factorial(k_channels) * (k_channels ** n_max_queue)) * p0
    Q = 1.0 - p_refusal
    A = arrival_rate * Q

    # 3. Длина очереди Lq
    p_k = (rho ** k_channels) / math.factorial(k_channels) * p0
    chi = rho / k_channels

    if chi == 1.0:
        Lq = p_k * n_max_queue * (n_max_queue + 1) / 2.0
    else:
        Lq = (
                (
                        p_k * chi *
                        (1.0 - (n_max_queue + 1) * (chi ** n_max_queue) + n_max_queue * (chi ** (n_max_queue + 1)))
                ) / (
                        (1.0 - chi) ** 2
                )
        )

    # 4. Характеристики количества заявок
    k_busy = rho * Q
    Ls = Lq + k_busy

    # 5. Временные характеристики (переводим из часов в минуты)
    Wq = (Lq / arrival_rate) * 60.0
    Ws = (Ls / arrival_rate) * 60.0
    W_obs = Ws - Wq

    # 6. Расчет финансовых потерь за период T
    total_loss = C_cost * arrival_rate * p_refusal * T_hours

    return {
        "rho": rho,
        "p0": p0,
        "p_refusal": p_refusal,
        "Q": Q,
        "A": A,
        "Lq": Lq,
        "k_busy": k_busy,
        "Ls": Ls,
        "Wq": Wq,
        "W_obs": W_obs,
        "Ws": Ws,
        "loss": total_loss
    }


def main():
    LAMBDA_H = 8
    T_MIN = 2
    K_CHANNELS = 6
    N_MAX_QUEUE = 5
    T_HOURS = 10
    C_COST = 75

    res = calculate_limited_queue_smo(
        lambda_h=LAMBDA_H,
        t_min=T_MIN,
        k_channels=K_CHANNELS,
        n_max_queue=N_MAX_QUEUE,
        T_hours=T_HOURS,
        C_cost=C_COST
    )

    print(f"\n=== Результаты расчета задачи 3 ===")
    print(f"Интенсивность нагрузки (rho): {res['rho']:.5f}")
    print(f"Вероятность простоя (P0): {res['p0']:.5f}")
    print(f"Вероятность отказа (P_отк): {res['p_refusal']:.5f}")
    print(f"Относительная пропускная способность (Q): {res['Q']:.5f}")
    print(f"Абсолютная пропускная способность (A): {res['A']:.5f} заявок/час")
    print(f"Среднее число заявок в очереди (Lq): {res['Lq']:.5f}")
    print(f"Среднее число занятых каналов (k_зан): {res['k_busy']:.5f}")
    print(f"Среднее число заявок в системе (Ls): {res['Ls']:.5f}")
    print(f"Среднее время ожидания в очереди (Wq): {res['Wq']:.5f} мин.")
    print(f"Среднее время обслуживания (W_обсл): {res['W_obs']:.5f} мин.")
    print(f"Среднее время пребывания в системе (Ws): {res['Ws']:.5f} min.")
    print(f"Потеря выручки за период {T_HOURS} ч.: {res['loss']:.2f} у.е.")


if __name__ == '__main__':
    main()
