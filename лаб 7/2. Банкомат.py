# Раздел 2. Жадные алгоритмы и динамическое программирование
# Листинг №2. Решение задачи №6 «Банкомат»


def count_change_ways(m: int, n: int, coins: list) -> int:
  # Таблица ДП для хранения количества способов набрать каждую сумму
  dp = [0] * (m + 1)
  dp[0] = 1  # Базовый случай: сумму 0 можно набрать 1 способом

  # Обход всех доступных достоинств купюр
  for coin in coins:
    for i in range(coin, m + 1):
      dp[i] += dp[i - coin]

  return dp[m]


if __name__ == "__main__":
  # Считывание входных данных
  m = int(input().strip())  # Сумма франков
  n = int(input().strip())  # Количество номиналов
  coins = list(map(int, input().strip().split()))  # Доинства купюр

  # Вычисление и вывод результата
  result = count_change_ways(m, n, coins)
  print(result)