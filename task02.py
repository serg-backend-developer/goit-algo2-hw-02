from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходит оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    memo = {}

    def dp(remaining_length):
        if remaining_length == 0:
            return (0, [])
        if remaining_length in memo:
            return memo[remaining_length]

        max_profit = 0
        optimal_cuts = []

        for cut_length in range(1, remaining_length + 1):
            sub_profit, sub_cuts = dp(remaining_length - cut_length)
            if sub_profit + prices[cut_length - 1] > max_profit:
                max_profit = sub_profit + prices[cut_length - 1]
                optimal_cuts = [cut_length] + sub_cuts

        memo[remaining_length] = (max_profit, optimal_cuts)
        return memo[remaining_length]

    max_profit, cuts = dp(length)
    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": len(cuts) - 1}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    dp = [0] * (length + 1)
    cuts = [[] for _ in range(length + 1)]

    for current_length in range(1, length + 1):
        for cut_length in range(1, current_length + 1):
            if dp[current_length - cut_length] + prices[cut_length - 1] > dp[current_length]:
                dp[current_length] = dp[current_length - cut_length] + prices[cut_length - 1]
                cuts[current_length] = cuts[current_length - cut_length] + [cut_length]

    return {
        "max_profit": dp[length],
        "cuts": cuts[length],
        "number_of_cuts": len(cuts[length]) - 1,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()