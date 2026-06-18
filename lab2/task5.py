import math


def calculate_engset_smo(n_sources, k_channels, t_service, target_percent, lambda_source=0.1):
    """
    Расчет замкнутой многоканальной СМО (модель Энгсета).
    n_sources: общее число источников (n)
    k_channels: число каналов обслуживания (k)
    t_service: время обслуживания одной заявки
    target_percent: порог активности источников в % (P)
    lambda_source: интенсивность генерации заявок ОДНИМ исправным источником
    """
    # Интенсивность обслуживания
    mu = 1.0 / t_service
    # Отношение интенсивностей
    alpha = lambda_source / mu

    def get_binomial_coeff(n, m):
        return math.factorial(n) // (math.factorial(m) * math.factorial(n - m))

    # Расчет P0
    sum_part1 = 0.0
    for m in range(k_channels + 1):
        sum_part1 += get_binomial_coeff(n_sources, m) * (alpha ** m)

    sum_part2 = 0.0
    for m in range(k_channels + 1, n_sources + 1):
        factor = math.factorial(m) / (math.factorial(k_channels) * (k_channels ** (m - k_channels)))
        sum_part2 += get_binomial_coeff(n_sources, m) * factor * (alpha ** m)

    p0 = 1.0 / (sum_part1 + sum_part2)

    # Расчет всех вероятностей состояний Pm
    probabilities = []
    for m in range(n_sources + 1):
        if m <= k_channels:
            pm = get_binomial_coeff(n_sources, m) * (alpha ** m) * p0
        else:
            factor = math.factorial(m) / (math.factorial(k_channels) * (k_channels ** (m - k_channels)))
            pm = get_binomial_coeff(n_sources, m) * factor * (alpha ** m) * p0
        probabilities.append(pm)

    # Средние характеристики
    Ls = sum(m * probabilities[m] for m in range(n_sources + 1))  # Среднее число неисправных

    # Среднее число занятых каналов
    k_busy = 0.0
    for m in range(n_sources + 1):
        if m <= k_channels:
            k_busy += m * probabilities[m]
        else:
            k_busy += k_channels * probabilities[m]

    Lq = Ls - k_busy  # Среднее число заявок в очереди

    # Расчет вероятности того, что активно >= P% источников
    # Число исправных источников = n_sources - m. Нам нужно, чтобы (n_sources - m) / n_sources >= target_percent / 100
    max_failed = int(n_sources * (1.0 - target_percent / 100.0))
    p_target_active = sum(probabilities[m] for m in range(max_failed + 1))

    return {
        "alpha": alpha,
        "p0": p0,
        "probabilities": probabilities,
        "Ls": Ls,
        "k_busy": k_busy,
        "Lq": Lq,
        "max_failed": max_failed,
        "p_target_active": p_target_active
    }


def main():
    N_SOURCES = 10
    K_CHANNELS = 5
    T_SERVICE = 2.5
    TARGET_PERCENT = 90
    LAMBDA_SOURCE = 0.1

    res = calculate_engset_smo(
        n_sources=N_SOURCES,
        k_channels=K_CHANNELS,
        t_service=T_SERVICE,
        target_percent=TARGET_PERCENT,
        lambda_source=LAMBDA_SOURCE
    )

    print(f"\n=== Результаты расчета задачи 5 ===")
    print(f"Коэффициент alpha (lambda/mu): {res['alpha']:.5f}")
    print(f"Вероятность простоя (P0): {res['p0']:.5f}")
    print(f"Среднее число неисправных источников (Ls): {res['Ls']:.5f}")
    print(f"Среднее число занятых наладчиков (k_зан): {res['k_busy']:.5f}")
    print(f"Среднее число заявок в очереди (Lq): {res['Lq']:.5f}")
    print(f"\nПроверка системного требования:")
    print(
        f"Максимально допустимое число неисправных источников для сохранения "
        f"{TARGET_PERCENT}% активности: {res['max_failed']}"
    )
    print(f"Вероятность того, что активно >= {TARGET_PERCENT}% источников: {res['p_target_active']:.5f}")


if __name__ == '__main__':
    main()
