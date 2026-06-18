import sys, io
from collections import deque

# Устанавливаем корректную кодировку для вывода в консоль
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def solve_johnson():
    # Исходные данные Варианта 3
    # Индексы задач: 0, 1, 2, 3, 4, 5, 6, 7
    duration_A = [5, 3, 9, 2, 7, 4, 6, 8]
    duration_B = [2, 6, 4, 8, 1, 5, 3, 7]
    num_jobs = len(duration_A)

    # Создаем список словарей для удобной фильтрации
    jobs = []
    for i in range(num_jobs):
        jobs.append({
            'id': i + 1,  # Номер задачи (1-индексация для отчета)
            'A': duration_A[i],
            'B': duration_B[i]
        })

    # Двусторонняя очередь для формирования оптимальной последовательности
    optimal_sequence = deque()

    # Копируем список задач, чтобы удалять распределенные
    remaining_jobs = list(jobs)

    while remaining_jobs:
        # Находим задачу с минимальным временем обработки на любой из стадий
        min_job = None
        min_val = float('inf')
        target_stage = 'A'

        for job in remaining_jobs:
            if job['A'] < min_val:
                min_val = job['A']
                min_job = job
                target_stage = 'A'
            if job['B'] < min_val:
                min_val = job['B']
                min_job = job
                target_stage = 'B'

        # Согласно правилу Джонсона:
        if target_stage == 'A':
            # Если минимум на стадии A — ставим в начало
            optimal_sequence.appendleft(min_job)
        else:
            # Если минимум на стадии B — ставим в конец
            optimal_sequence.append(min_job)

        # Удаляем распределенную задачу из списка оставшихся
        remaining_jobs.remove(min_job)

    # Превращаем в обычный список для удобства работы
    optimal_sequence = list(optimal_sequence)

    # Расчет временного графика (Makespan и Простой)
    time_A = 0
    time_B = 0
    idle_time_B = 0

    schedule_details = []

    for job in optimal_sequence:
        start_A = time_A
        end_A = start_A + job['A']
        time_A = end_A  # Стадия А работает непрерывно

        # Стадия Б может начать работу над задачей только после того,
        # как она завершилась на А И завершилась предыдущая задача на Б
        start_B = max(end_A, time_B)

        # Если стадия Б ждала задачу, фиксируем простой
        if start_B > time_B:
            idle_time_B += (start_B - time_B)

        end_B = start_B + job['B']
        time_B = end_B

        schedule_details.append({
            'id': job['id'],
            'start_A': start_A,
            'end_A': end_A,
            'start_B': start_B,
            'end_B': end_B
        })

    return optimal_sequence, schedule_details, time_B, idle_time_B


def print_task3(sequence, details, total_time, idle_time):
    print("\n" + "=" * 58)
    print("ЗАДАЧА 3: Оптимальное расписание Джонсона (Вариант 3)")
    print("=" * 58)

    seq_str = " -> ".join([f"ЛР{job['id']}" for job in sequence])
    print(f"\nОптимальный порядок обработки логов:\n  {seq_str}\n")

    print("Гант-таблица временных интервалов выполнения задач:")
    print("—" * 58)
    print(f"{'Задача':^8} | {'Стадия А (Обработка)':^21} | {'Стадия B (Индексация)':^21} |")
    print(f"{'':^8} | {'Начало':^10} {'Конец':^10} | {'Начало':^10} {'Конец':^10} |")
    print("—" * 58)

    for row in details:
        print(
            f" ЛР {row['id']:^4} | {row['start_A']:^10} {row['end_A']:^10} | {row['start_B']:^10} {row['end_B']:^10} |"
        )

    print("—" * 58)
    print(f"Общее время выполнения всего конвейера (Makespan): {total_time} ед.")
    print(f"Суммарное время простоя Стадии B (ожидание логов):  {idle_time} ед.")


def main():
    seq, det, total, idle = solve_johnson()
    print_task3(seq, det, total, idle)


if __name__ == '__main__':
    main()
