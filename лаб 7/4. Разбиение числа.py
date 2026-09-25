# Раздел 4. Метод поиска с возвратом (Backtracking)
# Листинг №4. Решение задачи №2 «Разбиение числа на слагаемые в неубывающем порядке»


def generate_partitions(n: int, start: int, current_partition: list):
  # Базовый случай: если остаток равен 0, выводим сформированное разбиение
  if n == 0:
    print(*current_partition)
    return

  # Перебор слагаемых в неубывающем порядке (от start до n)
  for i in range(start, n + 1):
    # Прямой ход: добавляем слагаемое
    current_partition.append(i)

    # Рекурсивный вызов для уменьшенного остатка
    generate_partitions(n - i, i, current_partition)

    # Обратный ход (backtracking): удаляем последнее слагаемое
    current_partition.pop()


if __name__ == "__main__":
  # Входные данные
  n = int(input().strip())

  # Запуск рекурсивного генератора
  generate_partitions(n, 1, [])