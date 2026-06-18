import math


def calculate_task6_smo(lambda_rate, t_service, k_channels, n_queue):
    """
    Расчет характеристик многоканальной СМО с ограничением на длину очереди.
    lambda_rate: интенсивность входящего потока (lambda)
    t_service: время обслуживания одной заявки (t)
    k_channels: число каналов обслуживания (k)
    n_queue: максимальное число мест в очереди (n)
    """
    arrival_rate = lambda_rate
    service_rate = 1.0 / t_service
    rho = arrival_rate / service_rate

    # Расчет вероятности простоя P0
    sum_k = sum((rho ** i) / math.factorial(i) for i in range(k_channels + 1))
    sum_n = sum((rho ** i) / (math.factorial(k_channels) * (k_channels ** (i - k_channels)))
                for i in range(k_channels + 1, k_channels + n_queue + 1))
    p0 = 1.0 / (sum_k + sum_n)

    # Вероятность отказа и пропускная способность
    p_refusal = (rho ** (k_channels + n_queue)) / (math.factorial(k_channels) * (k_channels ** n_queue)) * p0
    Q = 1.0 - p_refusal
    A = arrival_rate * Q

    # Вероятность наличия очереди (все каналы заняты)
    p_queue_exists = sum((rho ** i) / (math.factorial(k_channels) * (k_channels ** (i - k_channels))) * p0
                         for i in range(k_channels, k_channels + n_queue + 1))

    # Среднее число занятых и свободных каналов
    k_busy = rho * Q
    k_free = k_channels - k_busy

    # Длина очереди Lq
    p_k = (rho ** k_channels) / math.factorial(k_channels) * p0
    chi = rho / k_channels

    if chi == 1.0:
        Lq = p_k * n_queue * (n_queue + 1) / 2.0
    else:
        Lq = (
                     p_k * chi *
                     (1.0 - (n_queue + 1) * (chi ** n_queue) + n_queue * (chi ** (n_queue + 1)))
             ) / (
                     (1.0 - chi) ** 2
        )

    # Среднее число заявок в системе Ls
    Ls = Lq + k_busy

    # Временные характеристики
    W_q = Lq / arrival_rate
    W_obs = 1.0 / service_rate
    W_s = W_q + W_obs

    return {
        "rho": rho,
        "p0": p0,
        "p_queue_exists": p_queue_exists,
        "p_refusal": p_refusal,
        "Q": Q,
        "A": A,
        "k_busy": k_busy,
        "k_free": k_free,
        "Lq": Lq,
        "Ls": Ls,
        "W_q": W_q,
        "W_obs": W_obs,
        "W_s": W_s
    }


def main():
    K_CHANNELS = 5
    N_QUEUE = 25
    LAMBDA_RATE = 2.3
    T_SERVICE = 0.1

    res = calculate_task6_smo(
        lambda_rate=LAMBDA_RATE,
        t_service=T_SERVICE,
        k_channels=K_CHANNELS,
        n_queue=N_QUEUE
    )

    print(f"\n=== Результаты расчета задачи 6 ===")
    print(f"Интенсивность нагрузки (rho): {res['rho']:.5f}")
    print(f"1. Вероятность простоя (P0): {res['p0']:.5f}")
    print(f"2. Вероятность наличия очереди: {res['p_queue_exists']:.5f}")
    print(f"3. Вероятность отказа (P_отк): {res['p_refusal']:.5f}")
    print(f"4. Относительная пропускная способность (Q): {res['Q']:.5f}")
    print(f"5. Абсолютная пропускная способность (A): {res['A']:.5f}")
    print(f"6. Среднее число занятых каналов (k_зан): {res['k_busy']:.5f}")
    print(f"7. Среднее число свободных каналов (k_своб): {res['k_free']:.5f}")
    print(f"8. Среднее число заявок в очереди (Lq): {res['Lq']:.5f}")
    print(f"9. Среднее число заявок в системе (Ls): {res['Ls']:.5f}")
    print(f"10. Среднее время в очереди (Wq): {res['W_q']:.5f}")
    print(f"    Среднее время обслуживания (W_обсл): {res['W_obs']:.5f}")
    print(f"    Среднее время в системе (Ws): {res['W_s']:.5f}")


if __name__ == '__main__':
    main()
