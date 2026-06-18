import numpy as np


def calculate_decision_tree():
    # 1. Структура данных дерева решений
    # Описываем стратегии, их затраты и распределение исходов
    tree_data = {
        "Стратегия А (Быстрый релиз)": {
            "cost": 100,
            "env_states": {
                "Стабильная нагрузка (p=0.6)": {"prob": 0.6,
                                                "payoffs": {"Успех": (0.7, 1000), "Частичный успех": (0.2, 400),
                                                            "Провал": (0.1, -800)}},
                "Пиковая нагрузка (p=0.3)": {"prob": 0.3,
                                             "payoffs": {"Успех": (0.3, 1000), "Частичный успех": (0.4, 400),
                                                         "Провал": (0.3, -800)}},
                "Сбой инфраструктуры (p=0.1)": {"prob": 0.1,
                                                "payoffs": {"Успех": (0.0, 1000), "Частичный успех": (0.2, 400),
                                                            "Провал": (0.8, -800)}}
            }
        },
        "Стратегия Б (Дополнительное тестирование)": {
            "cost": 300,
            "env_states": {
                "Стабильная нагрузка (p=0.6)": {"prob": 0.6,
                                                "payoffs": {"Успех": (0.9, 900), "Частичный успех": (0.1, 300),
                                                            "Провал": (0.0, -900)}},
                "Пиковая нагрузка (p=0.3)": {"prob": 0.3,
                                             "payoffs": {"Успех": (0.7, 900), "Частичный успех": (0.2, 300),
                                                         "Провал": (0.1, -900)}},
                "Сбой infrastructure (p=0.1)": {"prob": 0.1,
                                                "payoffs": {"Успех": (0.4, 900), "Частичный успех": (0.4, 300),
                                                            "Провал": (0.2, -900)}}
            }
        },
        "Стратегия В (Отмена проекта)": {
            "cost": 0,
            "env_states": {
                "Любая нагрузка (p=1.0)": {"prob": 1.0, "payoffs": {"Заморозка бюджета": (1.0, 0)}}
            }
        }
    }

    results = {}

    print("\n" + "=" * 80)
    print("ПОЛНОЕ ДЕРЕВО РЕШЕНИЙ И ВЫЧИСЛЕНИЕ МЕТРИК:")
    print("=" * 80)
    print("[Корень: Выбор стратегии развития проекта]")

    for strat_name, strat_info in tree_data.items():
        cost = strat_info["cost"]
        print(f" └── {strat_name} (Затраты на реализацию: {cost})")

        # Шаг 1: Собираем плоский список финальных исходов для расчёта матожидания и риска
        flat_outcomes = []

        for env_name, env_info in strat_info["env_states"].items():
            p_env = env_info["prob"]
            print(f"     ├── Состояние: {env_name}")

            for outcome_name, (p_out, payoff) in env_info["payoffs"].items():
                total_prob = p_env * p_out
                final_profit = payoff - cost
                if total_prob > 0:
                    print(
                        f"     │   ├── {outcome_name:18s} | "
                        f"Итоговая вероятность: {total_prob:.3f} | "
                        f"Чистая прибыль: {final_profit}"
                    )
                    flat_outcomes.append({"prob": total_prob, "profit": final_profit})

        # Шаг 2: Расчёт EMV (Математическое ожидание чистой прибыли)
        emv = sum(item["prob"] * item["profit"] for item in flat_outcomes)

        # Шаг 3: Расчёт Дисперсии и Среднеквадратического отклонения (Риска)
        variance = sum(item["prob"] * ((item["profit"] - emv) ** 2) for item in flat_outcomes)
        std_dev = np.sqrt(variance)

        results[strat_name] = {"emv": emv, "risk": std_dev}
        print(f"     ИТОГ ДЛЯ ВЕТКИ -> Ожидаемая стоимость (EMV): {emv:.2f} | Уровень риска (Sigma): {std_dev:.2f}\n")

    print("=" * 80)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ СТРАТЕГИЙ:")
    print("=" * 80)
    for name, metrics in results.items():
        print(f"• {name}:")
        print(f"  Ожидаемая доходность (EMV) = {metrics['emv']:.2f}")
        print(f"  Абсолютный риск (Отклонение) = {metrics['risk']:.2f}")

    # Краткая автоматическая рекомендация
    best_emv_strat = max(results, key=lambda k: results[k]["emv"])
    min_risk_strat = min(results, key=lambda k: results[k]["risk"])

    print("\nЗАКЛЮЧЕНИЕ ДЛЯ ПРИНЯТИЯ РЕШЕНИЙ:")
    print(f" 1. По критерию максимальной средней прибыли (EMV) лучшим является: '{best_emv_strat}'")
    print(f" 2. По критерию минимального риска (наименьшая неопределенность) лучшим является: '{min_risk_strat}'")
    print("=" * 80)


def main():
    calculate_decision_tree()


if __name__ == "__main__":
    main()
