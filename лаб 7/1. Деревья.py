# Деревья
from collections import deque


class Node:

  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right

  def insert(self, new_value):
    if self.value is None:
      self.value = new_value
      return
    queue = deque([self])
    while queue:
      current = queue.popleft()
      if current.left is None:
        current.left = Node(new_value)
        return
      else:
        queue.append(current.left)
      if current.right is None:
        current.right = Node(new_value)
        return
      else:
        queue.append(current.right)


def is_mirror(t1: Node, t2: Node) -> bool:
  if t1 is None and t2 is None:
    return True
  if t1 is None or t2 is None:
    return False
  return (
      t1.value == t2.value
      and is_mirror(t1.left, t2.right)
      and is_mirror(t1.right, t2.left)
  )


def is_symmetric(root: Node) -> bool:
  if root is None:
    return True
  return is_mirror(root.left, root.right)


# создаем корень
root = Node(1)

# перечисляем остальные узлы по очереди сверху вниз, слева направо
tree_values = [2, 2, 4, 3, 3, 4]

for value in tree_values:
  root.insert(value)

print("Является ли дерево анаграммой:", is_symmetric(root))