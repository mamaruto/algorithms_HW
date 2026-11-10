from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, data=0, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# 1. Восстановление бинарного дерева из массива
def build_tree(arr: List[Optional[int]], i: int = 0) -> Optional[TreeNode]:
    """
    Массив хранит дерево по уровням (level-order), None означает пустое место.

    Связь родителя и потомка задаётся индексами: корень лежит в arr[0],
    левый потомок узла i лежит в arr[2*i + 1], правый в arr[2*i + 2],
    родитель узла i в arr[(i - 1) // 2].

    Узлы хранятся в объектах TreeNode, связанных ссылками left и right.
    Функция создаёт узел для arr[i] и рекурсивно строит его поддеревья.
    Рекурсия останавливается, когда индекс вышел за массив или узел пуст.

    Время O(n), память O(h) на стек рекурсии.
    """
    if i >= len(arr) or arr[i] is None:
        return None
    root = TreeNode(arr[i])
    root.left = build_tree(arr, 2 * i + 1)
    root.right = build_tree(arr, 2 * i + 2)
    return root


def build_tree_compact(values: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Вариант для формата, где дети пустых узлов не записываются:
    [1, None, 2, 3]. Формулы 2i+1 и 2i+2 здесь не работают.

    Используется очередь узлов, которым ещё не назначены дети. Из очереди
    берётся родитель, следующие два элемента массива становятся его левым
    и правым потомком, созданные потомки встают в конец очереди. Очередь
    выдаёт родителей в том же порядке, в каком они записаны в массиве.
    """
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        parent = queue.popleft()
        if values[i] is not None:
            parent.left = TreeNode(values[i])
            queue.append(parent.left)
        i += 1
        if i < len(values) and values[i] is not None:
            parent.right = TreeNode(values[i])
            queue.append(parent.right)
        i += 1
    return root


# 2. Симметричное бинарное дерево
def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    Рекурсивная проверка: левое поддерево должно быть зеркалом правого.

    Сравниваются пары узлов (a, b) на зеркальных позициях, начиная
    с (root.left, root.right):
      * оба пусты: пара симметрична;
      * пуст только один: дерево несимметрично;
      * иначе нужны a.data == b.data, зеркальность внешней пары
        (a.left, b.right) и внутренней пары (a.right, b.left).

    Корректность: отражение меняет местами левое и правое в каждом узле,
    поэтому два поддерева зеркальны тогда и только тогда, когда равны их
    корни и зеркальны внешние и внутренние дети. Рекурсия проверяет
    именно это определение для каждой пары.

    Время O(n), память O(h).
    """
    def mirror(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return (a.data == b.data
                and mirror(a.left, b.right)
                and mirror(a.right, b.left))

    return root is None or mirror(root.left, root.right)


def is_symmetric_bfs(root: Optional[TreeNode]) -> bool:
    """
    Итеративная проверка: обход по уровням, каждый уровень должен быть
    палиндромом. Узел level[i] сравнивается с level[n - 1 - i].

    Пустые потомки тоже кладутся в уровень как None. Без них уровни
    [2, None] и [None, 2] были бы неразличимы.
    """
    if root is None:
        return True
    level = [root]
    while level:
        n = len(level)
        for i in range(n // 2 + 1):
            a, b = level[i], level[n - 1 - i]
            if a is None and b is None:
                continue
            if a is None or b is None or a.data != b.data:
                return False
        next_level = []
        for node in level:
            if node is not None:
                next_level.append(node.left)
                next_level.append(node.right)
        level = next_level
    return True


# 3. Минимальная глубина
def min_depth_bfs(root: Optional[TreeNode]) -> int:
    """
    Минимальная глубина равна числу узлов на пути от корня до ближайшего листа.

    BFS обходит дерево по уровням: все узлы глубины 1, затем все узлы
    глубины 2 и так далее. Поэтому первый встреченный лист лежит ближе
    всех к корню: лист с меньшей глубиной был бы обработан раньше. Обход можно
    сразу остановить, не заходя в более глубокие ветви.
    """
    if root is None:
        return 0
    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0


def min_depth(root: Optional[TreeNode]) -> int:
    """
    DFS. Если у узла только одно поддерево, поиск идёт только по нему:
    на пустой стороне листа нет, и min с её глубиной 0 дал бы неверный ответ.
    """
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    if root.left is not None and root.right is not None:
        return 1 + min(min_depth(root.left), min_depth(root.right))
    if root.left is not None:
        return 1 + min_depth(root.left)
    return 1 + min_depth(root.right)


# 4. Произведение минимального и максимального элементов BST
def max_min_multiplication(data: List[Optional[int]]) -> int:
    """
    BST задан массивом с индексами потомков 2*i + 1 и 2*i + 2, поэтому
    восстанавливать дерево не требуется.

    В BST левое поддерево узла содержит только меньшие значения, правое
    только большие. Значит, минимум лежит в самом левом узле (от корня идём
    к левому потомку, пока он есть), а максимум в самом правом.

    Сложность O(h): каждый шаг спускается на один уровень без ветвлений
    и возвратов, поэтому шагов не больше высоты дерева h.
    """
    if not data or data[0] is None:
        raise ValueError("Пустое дерево")

    def descend(step: int) -> int:
        i = 0
        while True:
            child = 2 * i + step
            if child >= len(data) or data[child] is None:
                return i
            i = child

    return data[descend(1)] * data[descend(2)]


def max_min_multiplication_tree(root: TreeNode) -> int:
    """То же по восстановленному дереву: спуск по ссылкам left и right."""
    lo = hi = root
    while lo.left:
        lo = lo.left
    while hi.right:
        hi = hi.right
    return lo.data * hi.data


# 5. Сравнение двух бинарных деревьев
def is_same_tree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    """
    Деревья одинаковы, если для каждой пары соответствующих узлов:
      * оба пусты: ветви совпадают;
      * пуст только один: различается структура, деревья разные;
      * иначе значения равны, и одинаковы левые поддеревья
        (a.left, b.left) и правые поддеревья (a.right, b.right).

    Время O(min(n, m)), память O(h).
    """
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if a.data != b.data:
        return False
    return is_same_tree(a.left, b.left) and is_same_tree(a.right, b.right)


# Тесты
if __name__ == "__main__":
    # 1
    t = build_tree([8, 9, 11, 7, 16, 3, 1])
    assert (t.data, t.left.data, t.right.data) == (8, 9, 11)
    assert (t.left.left.data, t.left.right.data) == (7, 16)
    assert (t.right.left.data, t.right.right.data) == (3, 1)
    assert t.left.left.left is None
    g = build_tree([1, 2, None, 4, 5])
    assert g.right is None and (g.left.left.data, g.left.right.data) == (4, 5)
    assert build_tree([]) is None and build_tree([None]) is None
    c = build_tree_compact([1, None, 2, 3])
    assert c.left is None and c.right.data == 2 and c.right.left.data == 3
    assert is_same_tree(build_tree_compact([8, 9, 11, 7, 16, 3, 1]), t)
    assert build_tree_compact([]) is None
    print("1. build_tree: OK")

    # 2
    sym = build_tree([3, 8, 8, 9, 6, 6, 9])
    asym = build_tree([3, 7, 8, None, 9, 6, 9])
    cases = [
        (sym, True),
        (asym, False),
        (None, True),
        (build_tree([5]), True),
        (build_tree([1, 2, 2, None, 3, 3]), True),
        (build_tree([1, 2, 2, None, 3, None, 3]), False),  # одинаковые значения, разная структура
        (build_tree([1, 2, 2, 2, None, 2]), False),
        (build_tree([1, 2]), False),
        (build_tree([1, 2, 3]), False),
    ]
    for f in (is_symmetric, is_symmetric_bfs):
        for tree, expected in cases:
            assert f(tree) is expected, (f.__name__, expected)
    print("2. is_symmetric: OK")

    # 3
    md = build_tree([11, 8, 16, 2, 9, None, 6, 7, None, None, 9])
    chain = build_tree_compact([1, None, 2, None, 3, None, 4])
    for f in (min_depth, min_depth_bfs):
        assert f(md) == 3          # 11 -> 16 -> 6
        assert f(chain) == 4       # единственный лист в конце цепочки
        assert f(build_tree([1, 2])) == 2
        assert f(build_tree([1, 2, 3, 4])) == 2
        assert f(build_tree([1])) == 1
        assert f(None) == 0
    print("3. min_depth: OK")

    # 4
    bst = [16, 12, 18, 11, 15, 17, 21,
           None, None, None, None, None, None, 19, 24]
    assert max_min_multiplication(bst) == 11 * 24
    assert max_min_multiplication_tree(build_tree(bst)) == 11 * 24
    assert max_min_multiplication([5]) == 25
    assert max_min_multiplication([5, 3]) == 15            # нет правой ветви
    assert max_min_multiplication([5, None, 8]) == 40      # нет левой ветви
    assert max_min_multiplication([0, -4, 7, -9]) == -63
    print("4. max_min_multiplication: OK")

    # 5
    same1 = build_tree([16, 12, 18, None, 15, 17])
    same2 = build_tree([16, 12, 18, None, 15, 17])
    other = build_tree([16, 11, 18, None, 15, None, 21])
    assert is_same_tree(same1, same2)
    assert not is_same_tree(same1, other)
    assert not is_same_tree(build_tree([1, 2]), build_tree([1, None, 2]))
    assert not is_same_tree(build_tree([1, 2]), build_tree([1, 2, 3]))
    assert not is_same_tree(build_tree([1]), None)
    assert is_same_tree(None, None)
    print("5. is_same_tree: OK")

    print("\nВсе тесты пройдены.")
