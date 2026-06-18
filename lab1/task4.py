import numpy as np


# Справочник случайной согласованности Саати (RI)
RANDOM_CONSISTENCY_INDEX = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}


def calculate_weights_and_consistency(matrix):
    """
    Вычисляет вектор приоритетов (весов), lambda_max, CI и CR для матрицы сравнений.
    """
    n = matrix.shape[0]

    # 1. Вычисляем среднее геометрическое строк (классический метод Саати)
    geometric_mean = np.exp(np.mean(np.log(matrix), axis=1))
    weights = geometric_mean / np.sum(geometric_mean)

    # 2. Оценка согласованности
    # Вычисляем вектор произведения матрицы на веса Aw
    Aw = np.dot(matrix, weights)
    # Находим приближение к максимальному собственному значению lambda_max
    lambda_max = np.mean(Aw / weights)

    # Индекс согласованности (CI)
    if n > 1:
        ci = (lambda_max - n) / (n - 1)
    else:
        ci = 0.0

    # Отношение согласованности (CR)
    ri = RANDOM_CONSISTENCY_INDEX.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0.0

    return weights, lambda_max, cr


def interactive_matrix_input(size, default_matrix, title):
    """
    Обеспечивает красивый интерактивный построчный ввод матрицы сравнений.
    """
    print(f"\n{"=" * 64}")
    print(f"ФОРМИРОВАНИЕ МАТРИЦЫ: {title} ({size}x{size})")
    print("Вы можете вводить строки числами через пробел (например, '1 3 0.33')")
    print("Или просто нажмите ENTER, чтобы применить значения по умолчанию.")
    print(f"{"=" * 64}")

    first_line = input("Строка 1 (или ENTER для дефолта): ").strip()
    if not first_line:
        print(">> Выбран демонстрационный режим (матрица по умолчанию).")
        return default_matrix.copy()

    # Создаем пустую матрицу и заполняем первую строку
    matrix = np.eye(size)
    try:
        matrix[0, :] = [float(x) for x in first_line.split()]
        for i in range(1, size):
            line = input(f"Строка {i + 1}: ").strip()
            matrix[i, :] = [float(x) for x in line.split()]
        return matrix
    except Exception as e:
        print(f"Ошибка ввода ({e}). Применены дефолтные значения.")
        return default_matrix.copy()


def main():
    # Иерархия: Цель -> Выбор оптимального Message Broker для enterprise-системы
    criteria = ["Производительность (Throughput)", "Надежность (Reliability)", "Простота масштабирования",
                "Экосистема/Документация"]
    alternatives = ["Apache Kafka", "RabbitMQ", "NATS"]

    k = len(criteria)
    n = len(alternatives)

    # ---- ДЕФОЛТНЫЕ МАТРИЦЫ ДЛЯ ДЕМОНСТРАЦИИ ----
    # 1. Сравнение критериев друг с другом
    default_crit_matrix = np.array([
        [1.0, 3.0, 2.0, 5.0],
        [0.33, 1.0, 0.5, 3.0],
        [0.5, 2.0, 1.0, 4.0],
        [0.2, 0.33, 0.25, 1.0]
    ])

    # 2. Сравнение альтернатив по каждому критерию (список матриц)
    default_alt_matrices = [
        # По Производительности (Kafka > NATS > RabbitMQ)
        np.array([[1.0, 5.0, 2.0], [0.2, 1.0, 0.33], [0.5, 3.0, 1.0]]),
        # По Надежности (Kafka == RabbitMQ > NATS)
        np.array([[1.0, 1.0, 4.0], [1.0, 1.0, 4.0], [0.25, 0.25, 1.0]]),
        # По Масштабированию (Kafka > NATS > RabbitMQ)
        np.array([[1.0, 4.0, 1.5], [0.25, 1.0, 0.5], [0.66, 2.0, 1.0]]),
        # По Документации (RabbitMQ > Kafka > NATS)
        np.array([[1.0, 0.5, 3.0], [2.0, 1.0, 4.0], [0.33, 0.25, 1.0]])
    ]

    # ---- НАЧАЛО РАСЧЕТОВ ----
    # Шаг 1: Получаем и рассчитываем матрицу критериев
    crit_matrix = interactive_matrix_input(k, default_crit_matrix, "Сравнение критериев")
    crit_weights, _, crit_cr = calculate_weights_and_consistency(crit_matrix)

    print(f"\nВЕСА КРИТЕРИЕВ (Индекс согласованности CR = {crit_cr:.2%}):")
    for c, w in zip(criteria, crit_weights):
        print(f"  • {c}: {w:.4f}")

    if crit_cr > 0.10:
        print("ВНИМАНИЕ: Матрица критериев несогласована (CR > 10%)! Суждения требуют пересмотра.")

    # Шаг 2: Сравниваем альтернативы по каждому критерию
    # Матрица для хранения локальных весов: строки - альтернативы, столбцы - критерии
    local_weights_matrix = np.zeros((n, k))

    for i, criterion in enumerate(criteria):
        alt_matrix = interactive_matrix_input(n, default_alt_matrices[i], f"Альтернативы по критерию '{criterion}'")
        alt_weights, _, alt_cr = calculate_weights_and_consistency(alt_matrix)
        local_weights_matrix[:, i] = alt_weights

        print(f" Локальные веса для '{criterion}' (CR = {alt_cr:.2%}):")
        for alt, aw in zip(alternatives, alt_weights):
            print(f"    - {alt}: {aw:.4f}")

    # Шаг 3: Глобальный синтез приоритетов (перемножение матриц весов)
    global_priorities = np.dot(local_weights_matrix, crit_weights)

    # ---- ФИНАЛЬНЫЙ ВЫВОД ----
    print("\n" + "=" * 64)
    print("ИТОГОВЫЙ ГЛОБАЛЬНЫЙ СИНТЕЗ ПРИОРИТЕТОВ И ВЫБОР:")
    print("=" * 64)

    best_index = np.argmax(global_priorities)

    for i, alt in enumerate(alternatives):
        marker = "[РЕКОМЕНДУЕТСЯ]" if i == best_index else "  "
        print(f"{marker} {alt}: Итоговый глобальный вес = {global_priorities[i]:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
