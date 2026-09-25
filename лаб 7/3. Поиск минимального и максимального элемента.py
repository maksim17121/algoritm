# Раздел 3. Решение задач методом декомпозиции
# Листинг №3. Решение задачи №1 «Поиск минимального и максимального элемента»


def find_min_max(nums: list, low: int, high: int):
  # Базовый случай 1: подмассив состоит из одного элемента
  if low == high:
    return nums[low], nums[low]

  # Базовый случай 2: подмассив состоит из двух элементов
  if high == low + 1:
    if nums[low] < nums[high]:
      return nums[low], nums[high]
    else:
      return nums[high], nums[low]

  # Разделение: вычисление индекса середины отрезка
  mid = (low + high) // 2

  # Рекурсивный шаг: поиск экстремумов в левой и правой частях
  min_left, max_left = find_min_max(nums, low, mid)
  min_right, max_right = find_min_max(nums, mid + 1, high)

  # Объединение: определение общего минимума и максимума
  return min(min_left, min_right), max(max_left, max_right)


if __name__ == "__main__":
  # Входные данные из примера
  nums = [5, 7, 2, 4, 9, 6]

  # Вызов рекурсивной функции
  minimum, maximum = find_min_max(nums, 0, len(nums) - 1)

  # Форматированный вывод результатов
  print(f"The minimum array element is {minimum}")
  print(f"The maximum array element is {maximum}")