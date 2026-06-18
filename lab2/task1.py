import math


def calculate_erlang_smo(alpha_h, n_day, k_channels):
    """
    Вычисление характеристик многоканальной СМО с отказами.
    alpha_h: среднее время обработки (ч)
    n_day: заявок в сутки
    k_channels: число каналов для детального расчета
    """
    # 1. Расчет интенсивностей
    arrival_rate = n_day / 24.0  # lambda (заявок в час)
    service_rate = 1.0 / alpha_h  # mu (обслуживаний в час)
    rho = arrival_rate / service_rate  # интенсивность нагрузки

    # Функция для получения метрик при произвольном k
    def get_metrics(k):
        # Сумма для знаменателя P0
        sum_p = sum((rho ** i) / math.factorial(i) for i in range(k + 1))
        p0 = 1.0 / sum_p

        # Вероятность отказа (все k каналов заняты)
        p_refusal = (rho ** k) / math.factorial(k) * p0

        # Пропускная способность
        throughput_rel = 1.0 - p_refusal  # Q
        throughput_abs = arrival_rate * throughput_rel  # A

        # Загрузка каналов
        k_busy = rho * throughput_rel
        utilization = k_busy / k

        return p0, p_refusal, throughput_rel, throughput_abs, k_busy, utilization

    # Найти k_min, при котором Q >= 0.95
    k_min = 1
    while True:
        _, _, Q_temp, _, _, _ = get_metrics(k_min)
        if Q_temp >= 0.95:
            break
        k_min += 1

    # Расчет характеристик для заданного k
    p0, p_ref, Q, A, k_busy, k_util = get_metrics(k_channels)

    return {
        "rho": rho,
        "k_min": k_min,
        "p0": p0,
        "p_refusal": p_ref,
        "Q": Q,
        "A": A,
        "k_busy": k_busy,
        "k_util": k_util
    }


def main():
    ALPHA = 2.0
    N = 36
    K = 4

    res = calculate_erlang_smo(
        alpha_h=ALPHA,
        n_day=N,
        k_channels=K
    )

    print(f"\n=== Результаты расчета задачи 1 (Вариант: alpha={ALPHA}, n={N}, k={K}) ===")
    print(f"Интенсивность нагрузки (rho): {res['rho']:.3f}")
    print(f"1. Минимальное число каналов для Q >= 95%: {res['k_min']} каналов")
    print(f"\nХарактеристики для заданного k = {K}:")
    print(f"Предельная вероятность простоя (P0): {res['p0']:.5f}")
    print(f"Вероятность отказа (P_отк): {res['p_refusal']:.5f}")
    print(f"Относительная пропускная способность (Q): {res['Q']:.5f}")
    print(f"Абсолютная пропускная способность (A): {res['A']:.5f} заявок/час")
    print(f"Среднее число занятых каналов (k_зан): {res['k_busy']:.5f}")
    print(f"Коэффициент загрузки каналов (eta): {res['k_util']:.5f}")


if __name__ == "__main__":
    main()
